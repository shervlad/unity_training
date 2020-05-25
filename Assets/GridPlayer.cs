using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Collections.Generic;

public class GridPlayer : Agent
{

    public GameObject grid;
    GridController gridController;
    public override void Initialize(){
        gridController = grid.GetComponent<GridController>();
    }



    public override void OnActionReceived(float[] vectorAction){

        AddReward(1f);
    }


    public override void CollectObservations(VectorSensor sensor)
    {
        // Whether the penguin has eaten a fish (1 float = 1 value)
        // List<float> l = gridController.getFlatGrid();
        // Debug.Log($"Adding {l.FindAll(u => u==1f).Count} ones to the output!");
        // sensor.AddObservation(l);
        List<float> l = gridController.getLabels();
        Debug.Log($"Adding {l.FindAll(u => u>0f).Count} ones to the output!");
        sensor.AddObservation(l);
    }

    public override void Heuristic(float[] ActionsOut){
    }

}
