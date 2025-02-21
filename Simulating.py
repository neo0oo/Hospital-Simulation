import simpy
import random
def acitivity_generator(env,mean_registration,mean_consultation,Receptionist,Doctor,patient_id):
  time_entered_queue_registration = env.now
  print("---> Patient %s arrives to registration at %.2f" % (patient_id,time_entered_queue_registration))
  with Receptionist.request() as req:
    yield req
    time_left_queue_registration = env.now
    print("<--- Patient %s left registration queue at %.2f" % (patient_id, time_left_queue_registration))
    time_in_queue_registration = time_left_queue_registration - time_entered_queue_registration
    print("\\(0-0)/ Patient %s was waiting for %.2f minutes in registration queue" % (patient_id, time_in_queue_registration))
    registration_time = random.expovariate(1/mean_registration)
    yield env.timeout(registration_time)

  time_entered_queue_consultation = env.now

  with Doctor.request() as req:
    yield req
    time_left_queue_consultation = env.now
    time_in_queue_consultation = time_left_queue_consultation - time_entered_queue_consultation
    print("\\(0-0)/ Patient %s was waiting for %.2f minutes in consultation queue" % (patient_id, time_in_queue_consultation))

    consultation_time = random.expovariate(1/mean_consultation)
    yield env.timeout(consultation_time)

    decide_branch = random.uniform(0,1)
    if decide_branch < 0.25:
      time_entered_queue_surgery = env.now
      with Receptionist.request() as req:
        yield req
        time_left_queue_surgery = env.now
        time_in_queue_surgery = time_left_queue_surgery - time_entered_queue_surgery
        print("\\(0-0)/ Patient %s was waiting for %.2f minutes in surgery queue" % (patient_id, time_in_queue_surgery))
        book_surgery_time = random.expovariate(1/mean_book_surgery)
        yield env.timeout(book_surgery_time)
    else:
      print("Patient %s exited the system after the consultation" % (patient_id))


def patient_generator(env, wl_inter, mean_registration,mean_consultation, Doctor, Receptionist):
  patient_id = 1
  while True:
    wp = acitivity_generator(env,mean_registration,mean_consultation,Receptionist,Doctor,patient_id)
    env.process(wp)
    t = random.expovariate(1/wl_inter)
    yield env.timeout(t)
    patient_id += 1

random.seed(2023)
env = simpy.Environment()
Receptionist = simpy.Resource(env, capacity = 1)
Doctor = simpy.Resource(env, capacity= 2)
wl_inter = 3
mean_registration = 2
mean_consultation = 8
mean_book_surgery = 4
env.process(patient_generator(env,wl_inter, mean_registration,mean_consultation, Doctor, Receptionist))
env.run(until = 480)