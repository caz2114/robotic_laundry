#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/student/robotic_laundry/ros_ws/src/baxter_tools"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/student/robotic_laundry/ros_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/student/robotic_laundry/ros_ws/install/lib/python2.7/dist-packages:/home/student/robotic_laundry/ros_ws/build/baxter_tools/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/student/robotic_laundry/ros_ws/build/baxter_tools" \
    "/usr/bin/python" \
    "/home/student/robotic_laundry/ros_ws/src/baxter_tools/setup.py" \
    build --build-base "/home/student/robotic_laundry/ros_ws/build/baxter_tools" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/student/robotic_laundry/ros_ws/install" --install-scripts="/home/student/robotic_laundry/ros_ws/install/bin"
