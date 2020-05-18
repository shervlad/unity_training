using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StemDetach : MonoBehaviour
{
    // Start is called before the first frame update
    List<string> currentlyColliding;

    public GameObject agent;
    private bool isAttached;
    void Start()
    {
        currentlyColliding = new List<string>();
        isAttached = false;
        Debug.Log("Script Works"); 
    }

    // Update is called once per frame
    void Update()
    {
        FixedJoint fj = gameObject.GetComponent<FixedJoint>();
        // Debug.Log("Connected to: " + fj.connectedBody.name);
        bool gripperIsClosed = agent.GetComponent<RobotAgent>().gripperIsClosed;
        if(!isAttached && fj != null && fj.connectedBody.name == "UpperCylinder" 
            && currentlyColliding.Contains("left") && currentlyColliding.Contains("right")){
                
            Debug.Log("trying to reconnect...");
            // fj.connectedBody = agent.GetComponent<RobotAgent>().Palm.GetComponent<Rigidbody>();
            GetComponent<Rigidbody>().isKinematic = true;
            isAttached = true;
            GetComponent<Rigidbody>().transform.position = agent.GetComponent<RobotAgent>().Palm.transform.position;
            agent.GetComponent<RobotAgent>().AddReward(100f);
            Destroy(fj);
        }

        if(isAttached && !gripperIsClosed){
            GetComponent<Rigidbody>().isKinematic = false;
            isAttached = false;
        }

    }
    void FixedUpdate(){
        if(isAttached){
            Debug.Log("moving...");
            GetComponent<Rigidbody>().transform.position = agent.GetComponent<RobotAgent>().Palm.transform.position;
        }

    }
    private void OnCollisionEnter(Collision collision)
    {
        Debug.Log("Entered Collision");
        if (collision.transform.CompareTag("left"))
        {
            Debug.Log("LEFT");
            currentlyColliding.Add("left");
        }
        if (collision.transform.CompareTag("right"))
        {
            Debug.Log("RIGHT");
            currentlyColliding.Add("right");
        }
    }
    private void OnCollisionExit(Collision collision)
    {
        if (collision.transform.CompareTag("left"))
        {
            if(currentlyColliding.Contains("left"))
                currentlyColliding.Remove("left");
        }
        if (collision.transform.CompareTag("right"))
        {
            if(currentlyColliding.Contains("right"))
                currentlyColliding.Remove("right");
        }
    }
}
