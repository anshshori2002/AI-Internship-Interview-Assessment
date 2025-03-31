import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks):
        self.doctor_id = doctor_id
        self.queue = []  # Priority queue for patient management
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)]
        self.current_status = "Available"  # Track real-time doctor status
    
    def add_patient(self, patient):
        heapq.heappush(self.queue, (patient.priority, patient))
    
    def next_patient(self):
        if self.queue:
            patient = heapq.heappop(self.queue)[1]  # Fetch next patient
            patient.update_status("Consulting")  # Mark patient as consulting
            return patient
        return None
    
    def finish_consultation(self, patient):
        patient.update_status("Consulted")  # Mark patient as consulted
    
    def get_queue_length(self):
        return len(self.queue)
    
    def update_status(self, status):
        self.current_status = status  # Status: Available, Busy, Unavailable

class Patient:
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency
        self.source = source  # 'App', 'Walk-in', 'WhatsApp', etc.
        self.status = "Waiting"  # Default status
        self.priority = self.calculate_priority()
    
    def calculate_priority(self):
        # Higher urgency gets higher priority, walk-ins may have lower priority
        delay = max(0, (self.arrival_time - self.scheduled_time).seconds // 60)
        source_priority = {"App": 3, "Walk-in": 2, "WhatsApp": 1}  # Weighting factor
        return self.urgency * 10 - delay + source_priority.get(self.source, 0)
    
    def update_status(self, new_status):
        self.status = new_status  # Update patient status to "Arrived", "Consulting", "Consulted"
        print(f"Patient {self.patient_id} status updated to: {new_status}")

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}

    def add_doctor(self, doctor_id, availability_blocks):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks)

    def assign_patient(self, doctor_id, patient):
        if doctor_id in self.doctors:
            self.doctors[doctor_id].add_patient(patient)
            print(f"Patient {patient.patient_id} added to Doctor {doctor_id}'s queue.")

    def estimate_wait_time(self, doctor_id):
        if doctor_id in self.doctors:
            num_patients = self.doctors[doctor_id].get_queue_length()
            avg_consult_time = random.randint(8, 22)  # Simulating doctor-specific consult times
            return num_patients * avg_consult_time
        return None

    def notify_patient(self, patient, doctor_id):
        wait_time = self.estimate_wait_time(doctor_id)
        print(f"Notification to Patient {patient.patient_id}: Estimated wait time is {wait_time} minutes.")
        if wait_time > 30:
            print(f"Patient {patient.patient_id}, you can reschedule your appointment.")

    def process_next_patient(self, doctor_id):
        if doctor_id in self.doctors:
            doctor = self.doctors[doctor_id]
            patient = doctor.next_patient()
            if patient:
                print(f"Doctor {doctor_id} is consulting Patient {patient.patient_id}.")
                # Simulate consultation time
                consult_time = random.randint(8, 22)
                print(f"Consultation will take approximately {consult_time} minutes.")
                # After consultation, mark patient as consulted
                doctor.finish_consultation(patient)
                print(f"Patient {patient.patient_id} consultation completed.")

# Example Usage
qms = QueueManagementSystem()
qms.add_doctor(1, [(9, 12), (15, 18)])

patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

qms.assign_patient(1, patient1)
qms.assign_patient(1, patient2)

print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")

# Notify patients about wait time
qms.notify_patient(patient1, 1)
qms.notify_patient(patient2, 1)

# Process next patient
qms.process_next_patient(1)
qms.process_next_patient(1)
