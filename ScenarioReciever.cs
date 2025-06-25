using UnityEngine;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

public class ScenarioReceiver : MonoBehaviour
{
    private HttpListener listener;
    private CancellationTokenSource cts;

    void Start()
    {
        cts = new CancellationTokenSource();
        Task.Run(() => StartListener(cts.Token));
    }

    private async Task StartListener(CancellationToken token)
    {
        listener = new HttpListener();
        listener.Prefixes.Add("http://*:5000/");
        listener.Start();
        Debug.Log("HTTP Listener started on port 5000");

        while (!token.IsCancellationRequested)
        {
            var context = await listener.GetContextAsync();
            var request = context.Request;

            if (request.HttpMethod == "POST")
            {
                using (var reader = new System.IO.StreamReader(request.InputStream, request.ContentEncoding))
                {
                    string body = await reader.ReadToEndAsync();
                    Debug.Log("Received: " + body);

                    try
                    {
                        var json = JObject.Parse(body);
                        string command = json["command"]?.ToString();

                        switch (command)
                        {
                            case "play_sound":
                                string soundName = json["sound_name"]?.ToString();
                                PlaySound(soundName);
                                break;
                        }
                    }
                    catch
                    {
                        Debug.LogError("Invalid JSON or missing fields.");
                    }
                }

                var response = context.Response;
                string responseString = "OK";
                byte[] buffer = Encoding.UTF8.GetBytes(responseString);
                response.ContentLength64 = buffer.Length;
                var output = response.OutputStream;
                await output.WriteAsync(buffer, 0, buffer.Length);
                output.Close();
            }
            else
            {
                context.Response.StatusCode = 405;
                context.Response.Close();
            }
        }
    }

    void OnApplicationQuit()
    {
        cts.Cancel();
        listener.Stop();
        listener.Close();
    }

        void PlaySound(string name)
    {
        Debug.Log("Playing sound: " + name);
    }
}
