# robotic_laundry


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
