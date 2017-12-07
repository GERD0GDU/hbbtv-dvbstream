#! /usr/bin/env python

#
# Copyright  2010, mediatvcom (http://www.mediatvcom.com/), Claude Vanderm. Based on Lorenzo Pallara scripts (l.pallara@avalpa.com) 
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#                                  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#                                  
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os

from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *
from dvbobjects.MHP.AIT import *
from dvbobjects.HBBTV.Descriptors import *

#
# Shared values
#

max_service_count = 2 # TEST single

demo_transport_stream_id = 1 # demo value, an official value should be demanded to dvb org
demo_original_network_id = 1 # demo value, an official value should be demanded to dvb org

demo_service_id = [1,2] # demo value
pmt_pids = [201,202]
ait_pids = [501,502]

service_names = ["CHANNEL1","CHANNEL2"]


# parameters reported into the AIT to signalize a broadband application.
appli_name = "HBBTV Launcher (HBBTV Server)" #application name
appli_root = "http://rts1.cpa.local:8091/LaunchBar/" #URL base of transport_protocol_descriptor
#initial_path_bytes of simple application descriptor. 
# So the application path will be "http://rts1.cpa.local:8091/LaunchBar/index1.html"
# or "http://rts1.cpa.local:8091/LaunchBar/index2.html"
appli_paths = ["index1.html","index2.html"]  

organisationIds = [10,10]  # this is a demo value, dvb.org should assign an unique value
applicationIds  = [1001,1002] # this is a demo value. This number corresponds to a trusted application. 

# below, the video and audio PIDs reported into the PMT
video_pids = [2001,2002]
audio_pids = [2101,2102]

#
# Network Information Table
# this is a basic NIT with the minimum desciptors, OpenCaster has a big library ready to use
#
dvb_service_descriptor_loop_items = []

for i in range(0, max_service_count):
	dvb_service_descriptor_loop_items.append(
		service_descriptor_loop_item(
			service_ID = demo_service_id[i], 
			service_type = 1, # digital tv service type
		)
	)

nit = network_information_section(
	network_id = 1,
	network_descriptor_loop = [
		network_descriptor(network_name = "HBBTV-TEST",), 
	],
	transport_stream_loop = [
		transport_stream_loop_item(
			transport_stream_id = demo_transport_stream_id,
			original_network_id = demo_original_network_id,
			transport_descriptor_loop = [
				service_list_descriptor( #Optional
					dvb_service_descriptor_loop = dvb_service_descriptor_loop_items,
		    ),
			],		
		),
	],
	version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
	section_number = 0,
	last_section_number = 0,
)

#
# Program Association Table (ISO/IEC 13818-1 2.4.4.3)
#
program_loop_items = [
	program_loop_item(
		program_number = 0, # special program for the NIT
		PID = 16,
	)
]
# append all services
for i in range(0, max_service_count):
	program_loop_items.append(
		program_loop_item(
			program_number = demo_service_id[i],
			PID = pmt_pids[i],
		)
	)

pat = program_association_section(
	transport_stream_id = demo_transport_stream_id,
	program_loop = program_loop_items,
	version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
	section_number = 0,
	last_section_number = 0,
)

#
# Program Map Table (ISO/IEC 13818-1 2.4.4.8)
# this is PMT for HbbTV interactive applications
#
pmt = []

for i in range(0, max_service_count):
	pmt.append(
		program_map_section(
			program_number = demo_service_id[i],
			PCR_PID = video_pids[i], # usualy the same than the video
			program_info_descriptor_loop = [],
			stream_loop = [
				stream_loop_item(
					stream_type = 2, # mpeg2 video stream type
					elementary_PID = video_pids[i],
					element_info_descriptor_loop = []
				),
				stream_loop_item(
					stream_type = 3, # mpeg2 audio stream type
					elementary_PID = audio_pids[i],
					element_info_descriptor_loop = []
				),
				stream_loop_item(
					stream_type = 5, # AIT stream type
					elementary_PID = ait_pids[i],
					element_info_descriptor_loop = [ 
						application_signalling_descriptor(
							application_type = 0x0010, # HbbTV service
							AIT_version = 1,  # current ait version
						),
					]
				),		
			],
			version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
			section_number = 0,
			last_section_number = 0,
		)
	) 

#
# Service Description Table (ETSI EN 300 468 5.2.3) 
# this is a basic SDT with the minimum desciptors, OpenCaster has a big library ready to use
#
service_loop_items = []

for i in range(0, max_service_count):
	service_loop_items.append(
		service_loop_item(
			service_ID = demo_service_id[i],
			EIT_schedule_flag = 0, # 0 no current even information is broadcasted, 1 broadcasted
			EIT_present_following_flag = 0, # 0 no next event information is broadcasted, 1 is broadcasted
			running_status = 4, # 4 service is running, 1 not running, 2 starts in a few seconds, 3 pausing
			free_CA_mode = 0, # 0 means service is not scrambled, 1 means at least a stream is scrambled
			service_descriptor_loop = [
				service_descriptor(
					service_type = 1, # digital television service
					service_provider_name = "HBBTV",
					service_name = "HBBTV-" + service_names[i],
				),    
			],
		)
	)

sdt = service_description_section(
	transport_stream_id = demo_transport_stream_id,
	original_network_id = demo_original_network_id,
	service_loop = service_loop_items,
	version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
	section_number = 0,
	last_section_number = 0,
)

#
# Application Informaton Table (ETSI TS 101 812 10.4.6)
#
#
ait = []
for i in range(0, max_service_count):
	ait.append(
		application_information_section(
			application_type = 0x0010,
			common_descriptor_loop = [
				external_application_authorisation_descriptor(
				application_identifiers = [[organisationIds[i],applicationIds[i]]],
				application_priority    = [5]
				# This descriptor informs that 2 applications are available on the program by specifying the applications identifiers (couple of organization_Id and application_Id parameters) and their related priorities (5 for the first and 1 for the second).
				# Actualy our service contains only one application so this descriptor is not relevent and is just here to show you how to use this descriptor.
				# This descriptor is not mandatory and you could remove it (i.e. common_descriptor_loop = []).
				) 
			],
			application_loop = [
				application_loop_item(
					organisation_id = organisationIds[i],  # this is a demo value, dvb.org should assign an unique value
					application_id = applicationIds[i], 

					application_control_code = 1, 
					# 2 is PRESENT, the decoder will add this application to the user choice of application
					# 1 is AUTOSTART, the application will start immedtiatly to load and to execute
					# 7 is DISABLED, The application shall not be started and attempts to start it shall fail.
					# 4 is KILL, it will stop execute the application
					application_descriptors_loop = [
						transport_protocol_descriptor(
							protocol_id = 0x0003, # HTTP transport protocol
							URL_base = appli_root,
							URL_extensions = [],
							transport_protocol_label = 3, # HTTP transport protocol
						),  
						application_descriptor(
							application_profile = 0x0000,
							#0x0000 basic profile
							#0x0001 download feature
							#0x0002 PVR feature
							#0x0004 RTSP feature
							version_major = 1, # corresponding to version 1.1.1
							version_minor = 1,
							version_micro = 1,
							service_bound_flag = 1, # 1 means the application is expected to die on service change, 0 will wait after the service change to receive all the AITs and check if the same app is signalled or not
							visibility = 3, # 3 the applications is visible to the user, 1 the application is visible only to other applications
							application_priority = 1, # 1 is lowset, it is used when more than 1 applications is executing
							transport_protocol_labels = [3], # If more than one protocol is signalled then each protocol is an alternative delivery mechanism. The ordering indicates 
										 # the broadcaster's view of which transport connection will provide the best user experience (first is best)
						),
						application_name_descriptor(
							application_name = appli_name,
							ISO_639_language_code = "TUR"
						),
						simple_application_location_descriptor(initial_path_bytes = appli_paths[i]),		
					]
				),
			],
			version_number = 1,
			section_number = 0,
			last_section_number = 0,
		)
	)


#
# PSI marshalling and encapsulation
#
out = open("./tmp/nit.sec", "wb")
out.write(nit.pack())
out.close
out = open("./tmp/nit.sec", "wb") # python  flush bug
out.close
os.system('sec2ts 16 < ./tmp/nit.sec > ./output/nit.ts')

out = open("./tmp/sdt.sec", "wb")
out.write(sdt.pack())
out.close
out = open("./tmp/sdt.sec", "wb") # python   flush bug
out.close
os.system('sec2ts 17 < ./tmp/sdt.sec > ./output/sdt.ts')

out = open("./tmp/pat.sec", "wb")
out.write(pat.pack())
out.close
out = open("./tmp/pat.sec", "wb") # python   flush bug
out.close
os.system('sec2ts 0 < ./tmp/pat.sec > ./output/pat.ts')

for i in range(0, max_service_count):
	out = open("./tmp/pmt" + str(i) + ".sec", "wb")
	out.write(pmt[i].pack())
	out.close
	out = open("./tmp/pmt" + str(i) + ".sec", "wb") # python   flush bug
	out.close
	os.system('sec2ts ' + str(pmt_pids[i]) + ' < ./tmp/pmt' + str(i) + '.sec > ./output/pmt' + str(i) + '.ts')

	out = open("./tmp/ait" + str(i) + ".sec", "wb")
	out.write(ait[i].pack())
	out.close
	out = open("./tmp/ait" + str(i) + ".sec", "wb") # python   flush bug
	out.close
	os.system('sec2ts ' + str(ait_pids[i]) + ' < ./tmp/ait' + str(i) + '.sec > ./output/ait' + str(i) + '.ts')

#del out
#os.system('rm ./tmp/*.sec') # deleting of the section files.