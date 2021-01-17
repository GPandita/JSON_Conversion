# JSON_Conversion
- Converting tracker_wise grouped json file to frame_wise grouped json file

#### The input file (json) has the following structure:
```json
{
	“answer_key” : 
		{
			“video2d” : 
				{
					“data” : 
						{
							“trackers” : [T1, T2, T3 ……… Tn]
						}
				}
		}
}
```
                

- A single element in the list **answer_key -> video2d -> data -> trackers** represent a shape tracked across a video which is split into multiple frames.

#### Structure of a single Tracker element looks like the following :
```python
{
    _id : string,   # ->This is the tracker_id. 
    color: rgb(int, int, int) # -> Color of the shape tracked
    frames:
        {
            frame_id1 : annotation1,
            frame_id2 : annotation2,
        }
}
```

- In a single tracker element (type : dict), There are 3 keys, _id, color & frames. _id is the Tracker_ID. 
- The frames key in the tracker is of type dict. A single key value pair in the frames dict is frame_id & annotation pair. 

- The **transform.py** is to convert **answer_key -> video2d -> data -> trackers** to 
**answer_key -> video2d -> data -> frames**.
- Also it creates a csv file having the following structure :

frame_id  | tracking_id | label
------------- | ------------- | -------------
                     |                      |                    
