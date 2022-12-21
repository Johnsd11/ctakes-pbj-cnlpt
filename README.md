# cTAKES-PBJ-cnlpt:

### Building a Pipeline

`pipeline = pbj_pipeline.Pipeline()`<br>
- First we need to create a pipeline instance

`pipeline.add(ExampleNegation())`<br>
- Then we can add the programs we wish to use with pbj

`pipeline.add(ExampleTemporal())`<br>
- We can add more than one program

`pipeline.add(pbj_sender.PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))`<br>
- We now can add the pbj sender with the send_queue and host_name as mandatory arguments. The rest of the arguments have
defaults, but are editable. 

`pipeline.initialize()`<br>
- We add this line to initialize the pipeline, it isn't necessary but it's good practice.

`pbj_receiver.start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)`<br>
- Finally we start the pbj receiver which requries pipeline, receive_queue, and host_name as mandatory arguments; port_name
has a default, but is also editable.

# Building a Piperfile

### This is an example piper file that will spin up a complete pbj pipeline.
This piper will start the Apache Artemis broker pointed to by the -a parameter on the command line. It will pause for 5 seconds to allow artemis to fully launch. This piper will then launch another instance of Apache cTAKES. That instance of cTAKES will run the third and final bit of the entire pbj pipeline. This piper will then launch a python pbj bit of the entire pipeline.

`package org.apache.ctakes.pbj.ae`<br>
- Add this project's packages.

`cli ArtemisRoot=a`<br>
- Set the command line parameter -a to accept the directory of the Artemis installation.

`cli CommandDir=d`<br>
- Set the command line parameter -d to accept the directory of the Python installation.

`add ArtemisStarter Pause=5`
- Start the Artemis broker and pause 5 seconds.

`add CtakesRunner Pipe="-p org/apache/ctakes/pbj/pipeline/StartAllExample_end -o $OutputDirectory -a $ArtemisRoot"`
- Start another instance of cTAKES, running the pipeline in StartAllExample_end.piper

`add CommandRunner Command="python -m pip install ctakes-pbj" Wait=yes`<br>
`add CommandRunner Command="python ctakes-pbj-cnlpt\src\main\python\example_dtr_pipeline.py test/JavaToPython test/PythonToJava" LogFile=dtr_py.log`
- pip the dependency packages if your environment doesn't have them.

`set WriteBanner=yes`
- Writes a banner to let you know when ctakes starts and finishes.

`load DefaultTokenizerPipeline`
`load DictionarySubPipe`
- Load a simple token processing pipeline from another pipeline file

`add PbjSender SendQueue=test/JavaToPython SendStop=yes`
- Send CAS to Artemis at the specified queue.  Send stop signal when processing has finished.





    
