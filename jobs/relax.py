NumCycles = 4
OffAirWaitTime = 15 # time for pucks to go fuly off air and stop touching the primary
OnAirWaitTime = 15  # time for pucks to go back on air and the servo to stabilize

def run(sr):
    """Relax and re-home the SDSS primary mirror axial actuators (A, B and C)

    Save the current position of the axial actuators (A, B and C)
    Repeatedly do the following:
    - Move the axial actuators to the reverse limit, or, if the last cycle,
        home the axial actuators to avoid accumulation of error
    - Wait long enough for the pucks to release
    - Move back to the original position
    - Wait long enough for the mirror to get on air
    """
    yield sr.waitCmd('broadcast "relax: disabling collimation"')
    yield sr.waitCmd("process disable collimate")
    yield sr.waitCmd('broadcast "relax: saving current primary mirror actuator positions"')
    yield sr.waitCmd('talk prim "galil XQ#GETCMDP"')
    yield sr.waitCmd('talk prim "galil RELAXA=RESA; RELAXB=RESB; RELAXC=RESC"')
    for i in range(NumCycles):
        cycleNum = i + 1
        if cycleNum < NumCycles:
            yield sr.waitCmd('broadcast "relax: cycle %s/%s"' % (cycleNum, NumCycles))
            yield sr.waitCmd('talk prim/time=60 "galil A=RLIMA; B=RLIMB; C=RLIMC; XQ#MOVE"')
        else:
            yield sr.waitCmd('broadcast "relax: cycle %s/%s and homing"' % (cycleNum, NumCycles))
            yield sr.waitCmd('talk prim/time=60 "galil A=0; B=0; C=0; XQ#HOME"')
        yield sr.waitSec(OffAirWaitTime)
        yield sr.waitCmd('talk prim/time=60 "galil A=RELAXA; B=RELAXB; C=RELAXC; XQ#MOVE"')
        yield sr.waitSec(OnAirWaitTime)
    yield sr.waitCmd('broadcast/type=warning "enable collimation when you are done messing with the mirrors"')
