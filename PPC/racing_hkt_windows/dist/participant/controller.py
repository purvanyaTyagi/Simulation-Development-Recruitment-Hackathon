
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Path: list of waypoints [{"x": float, "y": float}, ...]
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"} 
# CmdFeedback: {"throttle", "steer"}         

# ─── CONTROLLER ───────────────────────────────────────────────────────────────
import numpy as np



def steering(path: list[dict], state: dict):

    L = 2.6  # vehicle wheelbase
    lookahead_dist = 5.0

    x = state["x"]
    y = state["y"]
    yaw = state["yaw"]

    target = None

    # find lookahead point
    for wp in path:
        dx = wp["x"] - x
        dy = wp["y"] - y
        dist = np.sqrt(dx**2 + dy**2)

        if dist > lookahead_dist:
            target = wp
            break

    if target is None:
        target = path[-1]

    dx = target["x"] - x
    dy = target["y"] - y

    alpha = np.arctan2(dy, dx) - yaw

    steer = np.arctan2(2 * L * np.sin(alpha), lookahead_dist)

    return np.clip(steer, -0.5, 0.5)


def throttle_algorithm(target_speed, current_speed, dt):

    Kp = 0.6
    error = target_speed - current_speed

    throttle = Kp * error
    brake = 0.0

    if throttle < 0:
        brake = -throttle
        throttle = 0

    return np.clip(throttle, 0.0, 1.0), np.clip(brake, 0.0, 1.0)

def control(
    path: list[dict],
    state: dict,
    cmd_feedback: dict,
    step: int,
) -> tuple[float, float, float]:
    """
    Generate throttle, steer, brake for the current timestep.
    Called every 50ms during simulation.

    Args:
        path:         Your planned path (waypoints)
        state:        Noisy vehicle state observation
                        x, y        : position (m)
                        yaw         : heading (rad)
                        vx, vy      : velocity in body frame (m/s)
                        yaw_rate    : (rad/s)
        cmd_feedback: Last applied command with noise
                        throttle, steer, brake
        step:         Current simulation timestep index

    Returns:
        throttle  : float in [0.0, 1.0]   — 0=none, 1=full
        steer     : float in [-0.5, 0.5]  — rad, neg=left
        brake     : float in [0.0, 1.0]   — 0=none, 1=full
    
    Note: throttle and brake cannot both be > 0 simultaneously.
    """
    throttle = 0.0
    steer    = 0.0
    brake = 0.0
   
    # TODO: implement your controller here
    steer = steering(path, state)
    target_speed = 5.0  # m/s, adjust as needed
    global integral
    throttle, brake = throttle_algorithm(target_speed, state["vx"], 0.05)

    return throttle, steer, brake
