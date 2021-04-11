# Honours experiment web app v2

| :file_folder: This project is archived. |
| --------------------------------------- |

This Flask web app was used as the main experimental platform during a user study for a Honours research project in 2014.

Basic functionality includes:

* Collecting demographic data via forms
* Storing user data in a localhost MySQL database
* Assigning users to an experimental condition based on existing data in the db
* Dynamically updating a page to transition between a series of text documents
* Automatically transitioning between documents after 45 seconds, with a countdown timer shown to users
* Integration with The Eye Tribe and Neulog APIs to automatically collect and store biometric data from these devices in real-time

## Basic setup

Requirements:

* Python2
* NodeJS
* [WebSocket proxy for The Eye Tribe Tracker](https://github.com/kzokm/eyetribe-websocket/)
* Flask
* Neulog API
* MySQL
* pymysql
* The Eye Tribe SDK

Notes:

* Built to run within Chrome

## Example usage

Some snippets to help save eyetracking data regularly during the experiment.

### In Flask views

```python
@app.route('/_dump_eyegaze',methods=['POST'])
def recordEye():
	try:
		with open(str(session['id'])+'.txt','w') as f: # Change output file to desired name & location
			json.dump(request.json,f)	# Writes to file
		return json.dumps({'status':'OK'}) # Returns OK to JS console
	except:
		return json.dumps({'status':'ERROR'}) # Returns ERROR to JS console
```

### In rendered HTML

```html
<script src="http://localhost:6556/eyetribe.js"></script>

<script>
$(document).ready(function() {

	var eyedata = []; // Create array to hold data over time
	
	EyeTribe.loop(function(frame) {
		if (paused) return;
		eyedata.push(frame.dump()); // Grab JSON dump from JS
		});
  
	$(function() {
		$('#submit').bind('click', function() { 
		
			$.ajax({ // Send to python for saving 
				url: '/_dump_eyegaze',
				data: JSON.stringify(eyedata),
				contentType: "application/json",
				type: 'POST',
				success: function(response) {
					console.log(response);
					},
				error: function(error) {
					console.log(error);
				}
			});
			
		});
	});
});
</script>
```