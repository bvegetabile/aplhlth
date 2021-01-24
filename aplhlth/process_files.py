import os
import sys
import csv
import datetime as dt
import xml.etree.ElementTree as ET

class apl_health_files:
	def __init__(self, fpath, verbose = True):
		self.folderpath = fpath 
		
		# Reading xml files on workouts
		self.xml = ET.parse(self.folderpath + 'export.xml')
		self.root = self.xml.getroot()
		self.types = set([c.tag for c in self.root])
		
		# Creating output directory
		if not os.path.exists(self.folderpath + "csv_outputs/"):
			os.mkdir(self.folderpath + "csv_outputs/")
			if verbose: sys.stdout.write('Created Directory: ' + self.folderpath + "csv_outputs/")
		self.csv_dir = self.folderpath + 'csv_outputs/'

		self.export_date = dt.datetime.strptime(self.root[0].attrib['value'], '%Y-%m-%d %H:%M:%S %z')
		# self.export_date = dt.datetime.strptime(self.export_date_string, '%Y-%m-%d %H:%M:%S %z')

		self.workouts = [c.attrib for c in self.root if c.tag == 'Workout']
		self.activities = [c.attrib for c in self.root if c.tag == 'ActivitySummary']
		self.records = [d.attrib for d in self.root if d.tag == 'Record']

		# Writing Activity History to File
		with open(self.csv_dir + '/activities.csv', 'w') as fout:
			act_writer = csv.writer(fout, delimiter=',')
			act_writer.writerow([k for k in self.activities[0].keys()])
			for r in self.activities:
				act_writer.writerow(list(r.values()))

		# Writing Workouts to file
		with open(self.csv_dir + '/workouts.csv', 'w') as fout:
			wo_writer = csv.writer(fout, delimiter=',')
			wo_headers = ['Created',
						  'WorkoutType', 
						  'Dur', 
                          'DurUnit', 
                          'Dist', 
                          'DistUnit', 
                          'Ener', 
                          'EnerUnit', 
                          'Start', 
                          'End', 
                          'Device']

			wo_writer.writerow(wo_headers)
			[wo_writer.writerow(self.parse_workout_line(w)) for w in self.workouts]

		with open(self.csv_dir + '/records.csv', 'w') as fout:
			r_writer = csv.writer(fout, delimiter=',')
			r_headers = ['creationDate',
						 'startDate',
						 'endDate',
						 'type',
						 'value',
						 'unit',
						 'sourceName',
						 'sourceVersion',
						 'device']
			r_writer.writerow(r_headers)
			[r_writer.writerow(self.parse_record(w, r_headers)) for w in self.records]

	def parse_workout_line(self, w):
		if 'device' in w.keys():
			device_val = w['device']
		else:
			device_val = 'NA'
		return [dt.datetime.strptime(w['creationDate'], '%Y-%m-%d %H:%M:%S %z'),
				w['workoutActivityType'][21:],
	    		float(w['duration']), 
	    		w['durationUnit'],
	    		float(w['totalDistance']),
	    		w['totalDistanceUnit'],	
	    		float(w['totalEnergyBurned']),
	    		w['totalEnergyBurnedUnit'],
	    		dt.datetime.strptime(w['startDate'], '%Y-%m-%d %H:%M:%S %z'),
	    		dt.datetime.strptime(w['endDate'], '%Y-%m-%d %H:%M:%S %z'),
	    		device_val]

	def parse_record(self, r, keyvals):
		return [r[h].replace('HKQuantityTypeIdentifier', '').replace('HKCategoryTypeIdentifier', '') if h in r.keys() else "NA" for h in keyvals]

