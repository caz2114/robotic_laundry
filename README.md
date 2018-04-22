# robotic_laundry

## notable changes
struct SDisplayParams is a wrapper for SRegion so Catherine combined them. 
```
struct SRegion
{
	double left;
	double right;
	double top;
	double bottom;
};

struct SDisplayParams
{
	SRegion region;
};
```

to 
```
SRegion = namedtuple('left','right','top','bottom')
```

## Files Completed 
-GarmentTemplate.py : Catherine

## Currently Working on
### Catherine
- Registration.py : 90% 
- dataTypes.py : 30% 
### Chris
- main.py
- objectSegmenter.py
- ImagePreprocessor.py
- ImageUtil.py
### Roop
- FoldPlanner.py -- pretty sure imports aren't working, look into. (.x,.y will likely error)
- main.py -- in progress

## Not completed
- ObjectSegmenter.py : Catherine in pipeline
- FoldPlanner.py

DistanceFields.cpp is replaced with sklearn's skfmm.distance function (https://pythonhosted.org/scikit-fmm/)



