using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CellController : MonoBehaviour
{
    public int ID;
    // Start is called before the first frame update
    public GameObject grid;
    private int collisions = 0;
    public string label;
    void Start()
    {
    } // Update is called once per frame
        void Update()
    {
        
    }

    public string Label(){
        if (doesCollide())
            return label;

        return "";
    }
    public bool doesCollide(){
        return (collisions > 0);
    }
    void OnTriggerEnter(Collider col){
        Debug.Log(" COLLISION!");
        collisions+=1;
        label = col.tag;
    }
    void OnTriggerExit(Collider col){
        Debug.Log("Exit Collision!");
        collisions-=1;
    }
}
    