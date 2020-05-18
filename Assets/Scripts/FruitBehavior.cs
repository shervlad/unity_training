using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FruitBehavior : MonoBehaviour
{
    public GameObject agent;
    // Start is called before the first frame update
    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "Basket")
        {
            Debug.Log("Good Job!");
            agent.GetComponent<RobotAgent>().AddReward(1000f);
            agent.GetComponent<RobotAgent>().EndEpisode();
            Destroy(gameObject);
            Destroy(this);
        }
        else if (collision.gameObject.name == "Ground")
        {
            Debug.Log("Oh no!");
            agent.GetComponent<RobotAgent>().AddReward(-100f);
            agent.GetComponent<RobotAgent>().EndEpisode();
            Destroy(gameObject);
            Destroy(this);
        }
    }
}
