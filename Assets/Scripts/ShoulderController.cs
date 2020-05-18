using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShoulderController : MonoBehaviour
{

    // Start is called before the first frame update

    public void MoveShoulder(float moveAmount){
        transform.Translate(transform.up*moveAmount,Space.Self);
        Vector3 clampedPosition = transform.localPosition;
        Debug.Log("Position:");
        Debug.Log(clampedPosition.ToString());

        clampedPosition.y = Mathf.Clamp(clampedPosition.y, 0.265f, 0.45f);
        transform.localPosition = clampedPosition;
    }
}
