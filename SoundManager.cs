using UnityEngine;
using System.Collections.Generic;

public class SoundManager : MonoBehaviour
{
    public List<NamedClip> clips;

    [System.Serializable]
    public class NamedClip
    {
        public string name;
        public AudioClip clip;
    }

    public void PlaySound(string name)
    {
        var found = clips.Find(c => c.name == name);
        if (found != null)
        {
            AudioSource newSource = gameObject.AddComponent<AudioSource>();
            newSource.clip = found.clip;
            newSource.Play();

            StartCoroutine(RemoveAudioSourceWhenDone(newSource));
        }
        else
        {
            Debug.LogWarning("Sound not found: " + name);
        }
    }

    private System.Collections.IEnumerator RemoveAudioSourceWhenDone(AudioSource source)
    {
        yield return new WaitForSeconds(source.clip.length);
        Destroy(source);
    }
}