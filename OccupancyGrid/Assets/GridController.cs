using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridController : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject prefabCell;
    private float cellSize=0.04f;
    private int gridSize=15;

    private GameObject[,,] cells;
    void Start()
    {
        setUp();
    }

    // Update is called once per frame
    void Update()
    {
        
    }


    public bool[,,] getGrid(){
        bool[,,] thisGrid = new bool[gridSize,gridSize,gridSize];
        for(int k=0;k<gridSize;k++){
            for(int j=0;j<gridSize;j++){
                for(int i=0;i<gridSize;i++){
                    thisGrid[i,j,k] = cells[i,j,k].GetComponent<CellController>().doesCollide();
                    // if(i==j && j==k){
                    //     thisGrid[i,j,k] = true;
                    // }
                }
            }
        }
        int xx = gridSize-1;
        thisGrid[0,0,0]  = true;
        thisGrid[xx,0,0] = true;
        thisGrid[0,xx,0] = true;
        thisGrid[0,0,xx] = true;
        return thisGrid;
    }
    public List<float> getFlatGrid(){
        bool [,,] thisGrid = getGrid();
        List<float> thisFlatGrid = new List<float>();
        for(int k=0;k<gridSize;k++){
            for(int j=0;j<gridSize;j++){
                for(int i=0;i<gridSize;i++){
                    if(thisGrid[i,j,k]){
                        thisFlatGrid.Add(1f);
                    }
                    else{
                        thisFlatGrid.Add(0f);
                    }
                }
            }
        }
        return thisFlatGrid;
    }
    public List<float> getLabels(){
        List<float> labelGrid = new List<float>();
        for(int k=0;k<gridSize;k++){
            for(int j=0;j<gridSize;j++){
                for(int i=0;i<gridSize;i++){
                    if(cells[i,j,k].GetComponent<CellController>().Label() == "red"){
                        labelGrid.Add(1f);
                    }
                    else if(cells[i,j,k].GetComponent<CellController>().Label() == "blue"){
                        labelGrid.Add(2f);
                    }
                    else{
                        labelGrid.Add(0f);
                    }
                }
            }
        }
        return labelGrid;
    }
    void setUp(){

        cells = new GameObject[gridSize,gridSize,gridSize];
        float x,y,z;
        for(int j=0;j<gridSize;j++){
            y = j*cellSize;
            for(int k=0;k<gridSize;k++){
                z = k*cellSize;
                for(int i=0;i<gridSize;i++){
                    x = i*cellSize;
                    cells[i,k,j] = Instantiate(prefabCell, new Vector3(x, y, z), Quaternion.identity);
                }
            }
        }
    }
}
