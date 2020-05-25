using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Collections.Generic;

public class RobotAgent : Agent
{
    public float moveSpeed = 5f;
    public float forwardSpeed = 0.2f;
    public float rotationSpeed = 3f;
    public float upDownSpeed = 0.2f;
    public float armExtendSpeed  = 0.1f;
    public float gripperCloseSpeed = 0.05f;
    public GameObject Environment;
    public GameObject Base;
    public GameObject Shoulder;
    public GameObject ForeArm;
    public GameObject LeftFinger;
    public GameObject RightFinger;
    public GameObject Palm;
    public GameObject Basket;

    public GameObject ropePrefab;
    Rigidbody baseRb;
    Rigidbody shoulderRb;
    Rigidbody foreArmRb;
    Rigidbody leftFingerRb;
    Rigidbody rIghtFingerRb;


    private GameObject goal;
    public bool gripperIsClosed;

    public GameObject grid;
    GridController gridController;

    public override void Initialize(){
    //     var children = areaOne.GetComponentsInChildren<Transform>();
    //     foreach (var child in children)
    //    if (child.name == whatYoureLookingFor)
    //         // do something
        baseRb        = Base.GetComponent<Rigidbody>();
        shoulderRb    = Shoulder.GetComponent<Rigidbody>();
        foreArmRb     = ForeArm.GetComponent<Rigidbody>();
        leftFingerRb  = LeftFinger.GetComponent<Rigidbody>();
        rIghtFingerRb = RightFinger.GetComponent<Rigidbody>();

        gridController = grid.GetComponent<GridController>();
    }

    public void MoveShoulder(float moveAmount){

        shoulderRb.transform.Translate(shoulderRb.transform.up*moveAmount,Space.Self);
        Vector3 clampedPosition = shoulderRb.transform.localPosition;
        clampedPosition.y = Mathf.Clamp(clampedPosition.y, 0.265f, 0.45f);
        shoulderRb.transform.localPosition = clampedPosition;
    }

    public void ExtendArm(float moveAmount){
        foreArmRb.transform.Translate(Vector3.forward*moveAmount);
        Vector3 clampedPosition = foreArmRb.transform.localPosition;
        clampedPosition.z = Mathf.Clamp(clampedPosition.z, -0.031f, 0.3f);
        foreArmRb.transform.localPosition = clampedPosition;
    }

    public void MoveGripper(float moveAmount){
        leftFingerRb.transform.Translate(moveAmount,0f,0f);
        Vector3 clampedPosition = leftFingerRb.transform.localPosition;
        clampedPosition.x = Mathf.Clamp(clampedPosition.x, -0.023874f, -0.008873949f);
        leftFingerRb.transform.localPosition = clampedPosition;

        rIghtFingerRb.transform.Translate(-moveAmount,0f,0f);
        clampedPosition = rIghtFingerRb.transform.localPosition;
        clampedPosition.x = Mathf.Clamp(clampedPosition.x, 0.004805954f, 0.019806f);
        rIghtFingerRb.transform.localPosition = clampedPosition;

        float epsilon = 0.0001f;
        if(leftFingerRb.transform.localPosition.x < -0.023874f + epsilon){
            gripperIsClosed = false;
        }
        else{
            gripperIsClosed = true;
        }
    }


    public override void OnActionReceived(float[] vectorAction){

        float scalingFactor = transform.localScale.x;


        float forwardAmount = scalingFactor*vectorAction[0]*forwardSpeed*Time.fixedDeltaTime;
        float upDown        = scalingFactor*vectorAction[1]*upDownSpeed*Time.fixedDeltaTime;
        float turnAction    = scalingFactor*vectorAction[2]*rotationSpeed*Time.fixedDeltaTime;
        float extendAction  = scalingFactor*vectorAction[3]*armExtendSpeed*Time.fixedDeltaTime;
        float gripperAction = scalingFactor*vectorAction[4]*gripperCloseSpeed*Time.fixedDeltaTime;

        baseRb.MovePosition(baseRb.transform.position + baseRb.transform.forward*forwardAmount);
        // shoulderRb.MovePosition(shoulderRb.transform.position + shoulderRb.transform.up*upDown);
        // shoulderRb.MoveRotation(shoulderRb.rotation*Quaternion.Euler(new Vector3(0,turnAction,0)));
        shoulderRb.transform.Rotate(shoulderRb.transform.up * turnAction);
        // shoulderRb.transform.Translate(shoulderRb.transform.up * upDown);
        // foreArmRb.transform.Translate(Vector3.forward*extendAction);
        MoveShoulder(upDown);
        ExtendArm(extendAction);
        MoveGripper(gripperAction);
        AddReward(-1f/MaxStep);



        float distToGoal = Vector3.Distance(goal.transform.position, Palm.transform.position);
        float distToBasket = Vector3.Distance(goal.transform.position, Basket.transform.position);
        AddReward(-distToGoal - distToBasket);
    }

    public override void Heuristic(float[] ActionsOut){

        float forwardAction = 0f;
        float upDown        = 0f;
        float turnAction    = 0f;
        float extendAction  = 0f;
        float gripperAction = 0f;

        if (Input.GetKey(KeyCode.W)){
            forwardAction = 1f;
        }
        else if(Input.GetKey(KeyCode.S)){
            forwardAction = -1f;
        }

        if (Input.GetKey(KeyCode.A)){
            turnAction = -1f;
        }
        else if(Input.GetKey(KeyCode.D)){
            turnAction = 1f;
        }

        if (Input.GetKey(KeyCode.I)){
            upDown = 1f;
        }
        else if(Input.GetKey(KeyCode.K)){
            upDown = -1f;
        }

        if (Input.GetKey(KeyCode.L)){
            extendAction = 1f;
        }
        else if(Input.GetKey(KeyCode.J)){
            extendAction = -1f;
        }
        if (Input.GetKey(KeyCode.E)){
            gripperAction = 1f;
        }
        else if(Input.GetKey(KeyCode.Q)){
            gripperAction = -1f;
        }

        ActionsOut[0] = forwardAction;
        ActionsOut[1] = upDown;
        ActionsOut[2] = turnAction;
        ActionsOut[3] = extendAction;
        ActionsOut[4] = gripperAction;
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        // Whether the penguin has eaten a fish (1 float = 1 value)

        // sensor.AddObservation(goal.transform.position - baseRb.transform.position);
        // sensor.AddObservation(goal.transform.position - Palm.transform.position);
        // sensor.AddObservation(shoulderRb.transform.localPosition);
        // sensor.AddObservation(shoulderRb.transform.localRotation.eulerAngles);
        // sensor.AddObservation(leftFingerRb.transform.localPosition);
        // sensor.AddObservation(rIghtFingerRb.transform.localPosition);

        List<float> l = gridController.getLabels();
        Debug.Log($"Adding {l.FindAll(u => u>0f).Count} ones to the output!");
        sensor.AddObservation(l);

    }


    private void RemoveOldRope(){
        foreach(Transform t in gameObject.transform.parent.transform){
            if(t.name == "Rope"){
                foreach(Transform tt in t){
                    Destroy(tt.gameObject);
                }
                Destroy(t.gameObject);
            }

        }
    }
    public override void OnEpisodeBegin()
    {
        RemoveOldRope();
        SetUp();
    }

    public void SetUp(){
        baseRb.transform.localPosition = new Vector3(0f,0.4f,0f);
        // shoulderRb.transform.rotation = new Quaternion(0f, 0f, 0f, 0f);

        // foreArmRb.localPosition = new Vector3(-0.0434f,0.66897f,-0.031f);

        Vector3 position  = new Vector3(5f,35f,35f);
        GameObject rope = Instantiate<GameObject>(ropePrefab,transform.parent.transform,false);
        rope.transform.localPosition = position;
        rope.name = "Rope";
        foreach(Transform t in rope.transform){
            if(t.name == "Sphere"){
                t.gameObject.GetComponent<FruitBehavior>().agent = gameObject;
            }
            if(t.name == "LowerCylinder"){
                t.gameObject.GetComponent<StemDetach>().agent = gameObject;
            }
        }

        GetGoal();

    }
    public void GetGoal(){
        foreach(GameObject g in GameObject.FindGameObjectsWithTag("goal")){
            if(g!=null && g.transform.IsChildOf(Environment.transform)){
                Debug.Log("FOUND GOAL!");
                goal = g;
            }
        }
    } 
}
