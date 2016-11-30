def convert_raw_bulb_info(val, prev, tolerance, m, b, max_converted, bulb_on = True, min_converted = 0):
	# Mapping from raw pot values to color values

	print("val = " + str(val))
	print("prev = " + str(prev))

	if val == None:
		val = 0

	val = float(val)
	converted = m * val - b
	converted = int(converted)
	print("initial converted = " + str(converted))

	# Eliminating extra potentiometer range
	if converted < 0:
		converted = 0
	if converted > max_converted:
		print("setting to max")
		converted = max_converted

	if (converted < (prev + tolerance)) and (converted > (prev - tolerance)):
		print("didn't depart from prev value enough")
		converted = prev
	else:
		print("value has changed")
		prev = converted

	if not bulb_on:
		print("setting converted to 0")
		converted = 0

	return converted, prev
