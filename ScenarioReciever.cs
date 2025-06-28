using UnityEngine;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using Newtonsoft.Json.Linq;
using System.Collections.Concurrent;

public class ScenarioReceiver : MonoBehaviour
{
    private HttpListener listener;
    private CancellationTokenSource cts;
    public SoundManager soundManager;

    private static ConcurrentQueue<System.Action> mainThreadActions = new ConcurrentQueue<System.Action>();

    void Start()
    {
        cts = new CancellationTokenSource();
        Task.Run(() => StartListener(cts.Token));
    }

    void Update()
    { 
        while (mainThreadActions.TryDequeue(out var action))
        {
            action?.Invoke();
        }
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

                        if (json["command"] == null)
                        {
                            Debug.LogWarning("Missing 'command' field in JSON.");
                            continue;
                        }

                        string command = json["command"].ToString();

                        switch (command)
                        {
                            case "play_sound":
                                if (json["sound_name"] == null)
                                {
                                    Debug.LogWarning("Missing 'sound_name' field for play_sound.");
                                    continue;
                                }
                                string soundName = json["sound_name"].ToString();

                                mainThreadActions.Enqueue(() => PlaySound(soundName));
                                break;

                            default:
                                Debug.LogWarning("Unknown command: " + command);
                                break;
                        }
                    }
                    catch (System.Exception ex)
                    {
                        Debug.LogError("Invalid JSON: " + ex.Message);
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
        soundManager.PlaySound(name);
    }
}
