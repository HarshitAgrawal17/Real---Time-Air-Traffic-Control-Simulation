# Real-Time Air Traffic Control Simulation

An event-driven simulator for aircraft in 3D airspace. Instead of stepping through time, it solves for the exact moment each flight is destroyed or lands, and answers status queries at any real-valued time.

*Individual assignment for a Programming with Data Structures course at IIT Delhi (2026).*

## Problem

Aircraft move over a flat earth with no gravity, accelerating only when the controller sends an acceleration vector. Between instructions, each flight follows constant-acceleration motion in real-valued time. A flight ends permanently in one of these ways:

- **Structural damage:** its speed strictly exceeds its maximum speed.
- **Ground crash:** its height reaches zero while it is still descending.
- **Collision:** it is at exactly the same position as another active flight.
- **Safe landing:** it is at z = 0 with zero velocity and zero acceleration.

Ended flights stop moving, ignore instructions and cannot collide with anything. At any instant, damage, crashes and landings are applied before collisions.

## Approach

**Single flight (`Flight`).** Each flight stores its position, velocity and acceleration as of the last instruction. It computes the end time of the flight once per instruction:
- Squared speed and height are quadratics in the time since the last instruction, so the time the speed limit is exceeded and the time the ground is reached are found by solving quadratics.
- The earlier of the two decides whether the flight ends in damage, a crash or a safe landing, with special cases for flights that touch z = 0 at zero vertical velocity and keep moving horizontally.

**Many flights (`AirTrafficControl`).** After each `create` or `update`, collision times are recomputed for all active flights:
- For each pair, relative position is a quadratic in each of x, y and z, so the pair collides only at a time when all three roots agree. A coordinate that is identically zero is treated as true at all times.
- Collisions only count before either flight's own end time, so an earlier accident correctly removes a flight from a later collision.
- The earliest collision time among all pairs is found. Every flight involved at that instant is marked, removed from consideration, and the search repeats on the remaining flights, so three or more flights colliding at the same point are handled together.

**Status** compares the query time with each flight's end time and collision time, whichever is earlier.

All floating-point comparisons use a tolerance of 1e-6 (`is_equal`, `is_less`, and so on).

## Complexity

Recomputing collisions checks every pair of active flights, so each instruction costs roughly O(F²) for F active flights, or more if several collision rounds are needed. Per-flight events are O(1).

## Interface

```python
Flight(max_speed, position, velocity)
flight.set_acceleration(time, (ax, ay, az))
flight.status(time)            # "flying" | "accident" | "landed safely"

AirTrafficControl()
atc.create(time, flight_id, max_speed, position, velocity)
atc.update(time, flight_id, acceleration)
atc.status(time, flight_id)    # also "does not exist" for unknown ids
```

## Example

A flight starts at height 4 at rest and is told to accelerate downward at 2:

```python
from student_code import Flight

f = Flight(10, (0, 0, 4), (0, 0, 0))
f.set_acceleration(0, (0, 0, -2))
f.status(1)   # "flying"    (height 3)
f.status(3)   # "accident"  (hit the ground at t = 2 while descending)
```
