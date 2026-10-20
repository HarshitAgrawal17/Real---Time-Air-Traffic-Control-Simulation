import math
EPS = 1e-6

def is_equal(x, y):
    """Return True when x and y should be treated as equal."""
    return abs(x - y) <= EPS
def is_less(x, y):
    """Return True when x is definitely smaller than y."""
    return x < y - EPS
def is_greater(x, y):
    """Return True when x is definitely greater than y."""
    return x > y + EPS
def is_less_equal(x, y):
    """Return True when x should be treated as less than or equal to y."""
    return not is_greater(x, y)
def is_greater_equal(x, y):
    """Return True when x should be treated as greater than or equal to y."""
    return not is_less(x, y)
    
class Flight:
    """A single aircraft."""
    def __init__(self, max_speed, position, velocity = (0,0,0), time = 0):
        self._max_speed = max_speed
        self._pos = position
        self._v = velocity
        self._a = (0,0,0)
        # self._time is the time when last accelaration call was made
        # Similarly, self. a,v,pos are also at the time when the call was made
        self._time = time
   
        self._coll = float('inf')
        if velocity == (0,0,0) and position[2] == 0:
            self._reason = 'landed safely'
            self._end = time
        elif velocity[2] < 0 and position[2] == 0:
            self._reason = 'accident'
            self._end = time
        else:
            self._reason = 'flying'
            self._end = float('inf')
            self.done_with_you()


      
        
        """
        max_speed : int, the highest speed this flight may hold
        position : a tuple (x, y, z) of integers, where it starts
        velocity : a tuple (vx, vy, vz) of integers, its initial velocity
        
        A newly created flight has the given initial velocity and acceleration
        (0, 0, 0). Its status must already be correct at the moment it is
        created.
        """
    def speed(self,time):
        V = self.vel_t(time)
        return math.sqrt(sum(l**2 for l in V))
        
    def vel_t(self,time): #Velocity at any time t
        if is_less_equal(time, self._end):
            vel = tuple(self._v[i] + self._a[i]*(time - self._time) for i in range(3))
            
            return vel
        
    def pos_t(self,time):
        if is_less_equal(time, self._end):
            return tuple((self._pos[i] + self._v[i]*(time - self._time) + 1/2 * self._a[i]*((time - self._time)**2) ) for i in range(3))

    def exceeds_max_speed(self):
        current_speed = self.speed(self._time)
        if is_greater(current_speed, self._max_speed):
            return 0
        if self._a == (0,0,0):
            return float('inf')
        else:
            #Time t0 when speed exceeds max speed
            a = self.speed(self._time)**2
            b = sum(self._a[i] * self._v[i] for i in range(3))
            c = sum(l**2 for l in self._a)
            #polynomial t2 + 2b/c t + a-max_speed**2/c
            B = 2*b/c 
            C = (a-self._max_speed**2)/c
            D=B*B -4*C
            if is_greater_equal(D,0):
                root_D = math.sqrt(D)
                t_a = (-B - root_D)/2
                t_b = (-B + root_D)/2
                if is_greater_equal(t_a,0):
                    t0 = t_a
                elif is_greater_equal(t_b,0):
                    t0 = t_b
                else: t0 = float('inf')
            else: t0 = float('inf')
                   
            return t0
            
    def altitude_0(self):
        if is_equal(self._pos[2],0):
            if is_less(self._v[2], 0) or (is_equal(self._v[2], 0) and is_less(self._a[2],0)):
                return 0
            if self._a[2] >= 0:
                return float('inf')
            
            
        if self._a[2] == 0:
            if is_equal(self._v[2],0):
                return float('inf')                  
            else:
                t = -self._pos[2]/self._v[2]  
                return t if is_greater(t,0) else float('inf')  
            
        else:
            az = self._a[2]
            vz = self._v[2]
            if is_less( D:= (4*(vz**2) - 8*self._pos[2]*az) , 0):
                return float('inf')
            else:
                x = -2 * vz / az
                t_1 = (x - math.sqrt(D)/az)/2
                t_2 = (x + math.sqrt(D)/az)/2
                t1 = None
                if is_greater_equal(t_1,0):
                    t1 = t_1
                else:
                    if is_greater_equal(t_2,0):
                        t1 = t_2
                return t1 if t1 is not None else float('inf')
        
    def done_with_you(self):
        if is_equal(self._pos[2], 0) and all(is_equal(c, 0) for c in self._v) and self._a == (0, 0, 0):
            self._end = self._time
            self._reason = 'landed safely'
            return
        
        time_max = self.exceeds_max_speed()
        time_z_0 = self.altitude_0()
        time_end = min(time_max, time_z_0)
        
        if time_end == float('inf'):
            self._end = time_end
            self._reason = 'flying'
        else:
            self._end = self._time + time_end    
            V = self.vel_t(self._end)
            A = self._a
            if is_equal(time_max , time_end) and is_less(time_max , time_z_0):
                self._reason = 'accident'
                
            else: #z becomes 0 first
                #Hits ground and everything becomes zero --> safe landing
                if is_equal(V[2], 0) and is_equal(V[1], 0) and is_equal(V[0], 0) and A == (0,0,0):
                    self._reason = 'landed safely'
                    
                #Lands safely but is still in motion
                elif is_equal(V[2], 0) and is_greater_equal(A[2],0):
                    if time_max == float('inf'):
                        self._end = float('inf')
                        self._reason = 'flying'
                    else:
                        self._end = self._time + time_max
                        self._reason = 'accident'
                    
                else:
                    self._reason = 'accident'
                
    def set_acceleration(self, time, acceleration):
        if is_less(time, self._end):    
            new_pos = self.pos_t(time)
            new_v = self.vel_t(time)
            self._pos = new_pos
            self._v = new_v
            self._time = time
            self._a = acceleration
            #To reset all collision end times, important for other flights too
         
            #Anyways, we are calculating new end time b
            
            #self._end = self._time + min(self.exceeds_max_speed() , self.altitude_0())
        
            self.done_with_you()
        #If flight cant crash, status remains flying
        #If it is about to end at sometime, it modifies end time
        # and reason: accident or landed or might br flying if x and y dorection are non zero, wtf
       
        
        
        """
        time : the instant from which the new acceleration applies
        acceleration : a tuple (ax, ay, az) of integers
        
        A flight that has already finished ignores this instruction.
        """
        
    def status(self, time):
        if is_less(time,min(self._end, self._coll)):
            self._status = 'flying'
            return self._status
        #ended earlier than collision
        if is_less_equal(self._end, self._coll):
            return self._reason
        return 'accident'
            
        
        """
        Return this flight’s status at the given instant: "flying",
        "accident" or "landed safely".
        """

class AirTrafficControl:
    """The controller, which owns every flight."""

    def __init__(self):
        """Start a new session, with no flights, at time 0."""
        self._time = 0
        self._flights = {}
    def create(self, time, flight_id, max_speed, position, velocity):
        self._time = time
        self._flights[flight_id] = Flight(max_speed, position, velocity,time)
        self._flights[flight_id]._time = time
        self.recompute(time)
        
        """Create a flight with the given position and initial velocity."""
    #Flight ids of active flights    
    def active_flights(self, time):
        l = list(i for i in self._flights if self._flights[i].status(time)=='flying') 
        return l

    def update(self, time, flight_id, acceleration):
        f = self._flights.get(flight_id)
        if f is None:
            return
        if f.status(time) != 'flying':
            return
        self._time = time
        f.set_acceleration(time, acceleration)
        self.recompute(time)


    def status(self, time, flight_id):
        if flight_id in self._flights:
            return self._flights[flight_id].status(time)
        else:
            return 'does not exist'
        
        
        """
        Return the status of the given flight at the given instant: "flying",
        "accident", "landed safely", or "does not exist" if no flight with
        that identifier has ever been created.
        """
    
    def recompute(self,time):  
        Active_ids = self.active_flights(time)
        for i in Active_ids:
            self._flights[i]._coll = float('inf')
            
        
        remaining = set(Active_ids)
        while True:
            best_time = float('inf')
            best_group = set()
            rem_list = list(remaining)
            for a in range(len(rem_list)):
                for b in range(a + 1, len(rem_list)):
                    id_a, id_b = rem_list[a], rem_list[b]
                    fa, fb = self._flights[id_a], self._flights[id_b]
                    
                    times = self.collision(fa, fb, time)
                    if not times:
                        continue
                    tmin = min(times)
                    if is_less(tmin, best_time):
                        best_time = tmin
                        best_group = {id_a, id_b}
                    elif is_equal(tmin, best_time):
                        best_group.add(id_a)
                        best_group.add(id_b)
 
            if best_time == float('inf') or not best_group:
                break
 
            for i in best_group:
                self._flights[i]._coll = best_time
            remaining -= best_group
            if len(remaining) < 2:
                break
      #Returns set of times    
    def collision(self, f1:Flight, f2:Flight, time): #Returns set of times
        e1 = f1._end
        e2 = f2._end
        upper_bound = min(e1,e2)
        if is_less(time,upper_bound ):
            #Collision can happen
            t = self._time
            p1 = f1.pos_t(t)
            p2 = f2.pos_t(t)
            v1 = f1.vel_t(t)
            v2 = f2.vel_t(t)
            a1 = f1._a
            a2 = f2._a
            
            p = tuple(p1[i] - p2[i] for i in range(3))
            v = tuple(v1[i] - v2[i] for i in range(3))
            a = tuple(a1[i] - a2[i] for i in range(3))
            
            #Finally, p has to become 0
            # s = -p
            # -p = ut + 1/2 at2
            


            # INSIDE collision()
            tx = self.solve_polynomial(p[0], v[0], a[0])
            ty = self.solve_polynomial(p[1], v[1], a[1])
            tz = self.solve_polynomial(p[2], v[2], a[2])
            
            t_col = []
            time_uncompared = set()
            
            # Case 1: All three are ALL_TIME
            if tx == ['ALL_TIME'] and ty == ['ALL_TIME'] and tz == ['ALL_TIME']:
                time_uncompared = {self._time}
                
            # Case 2: tx is ALL_TIME (loop ty and tz)
            elif tx == ['ALL_TIME']:
                if ty == ['ALL_TIME']:
                    time_uncompared = set(tz)
                elif tz == ['ALL_TIME']:
                    time_uncompared = set(ty)
                else:
                    for t in ty:
                        for T in tz:
                            if is_equal(t, T):
                                t_col.append(t)
                    time_uncompared = set(t_col) if t_col else {float('inf')}

            # Case 3: ty is ALL_TIME (loop tx and tz)
            elif ty == ['ALL_TIME']:
                if tz == ['ALL_TIME']:
                    time_uncompared = set(tx)
                else:
                    for t in tx:
                        for T in tz:
                            if is_equal(t, T):
                                t_col.append(t)
                    time_uncompared = set(t_col) if t_col else {float('inf')}

            # Case 4: tz is ALL_TIME (loop tx and ty)
            elif tz == ['ALL_TIME']:
                for t in tx:
                    for T in ty:
                        if is_equal(t, T):
                            t_col.append(t)
                time_uncompared = set(t_col) if t_col else {float('inf')}

            # Case 5: None are ALL_TIME (Loop all three)
            else:
                for t in ty:
                    for T in tz:
                        if is_equal(t, T):
                            for x in tx:
                                if is_equal(t, x):
                                    t_col.append(t)
                time_uncompared = set(t_col) if t_col else {float('inf')}
   
        else:
            time_uncompared = set([float('inf')])
            
        valid = { t for t in time_uncompared if is_less(t,upper_bound) }
        return valid
    
    def solve_polynomial(self, p,v,a): #returns atmost 2 times as list
        if a == 0:
            if is_equal(v,0):
                if is_equal(p,0):
                    #It remains valid for all time
                    #What to return now
                    return ['ALL_TIME']
                else:
                    return [float('inf')]
            else:
                return [self._time + (-p/v)] if is_greater_equal(-p/v , 0) else [float('inf')]
        else:
            D = (v*v - 2*a*p) #Actually it is D/4
            if is_less(D,0):
                return [float('inf')]
            else:
                t1 = (-v - D**(1/2))/a
                t2 = (-v + D**(1/2))/a
                x = []
                if is_greater_equal(t1, 0): x.append(t1+self._time)
                if is_greater_equal(t2, 0): x.append(t2+self._time)
                return x if x!=[] else [float('inf')]
                

            
