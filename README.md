### **Prerequisites**

Make sure your system has the following installed before installing the project:

•Git
•Python 3.11+
•Pip
•Node,js 18+
•Ngrok (Production)
•Vercel (for App Deployment in Production)

### **Downloading**

The project can be found at the following GitHub repository https://github.com/kye-li/twitter-viz-fyp.git. To run the project, clone the repository into your system.

### Server

#### Preparation:

After the project repository is cloned, navigate to “ /backend”. 
From here run:

pip install -r requirements.txt


#### Running:

**Development**

To run the application in a development environment, navigate to “ /backend” and run:
python appRoutes.py

This will start the server, which is hosted on http://127.0.0.1:5049.
All API endpoints could be found on http://127.0.0.1:5049/docs. 

**Production**

Open the ngrok application installed on your computer. 
In the ngrok agent, run:
ngrok http http://127.0.0.1:5049

(Note: without an account, the server would only be hosted on the same domain for 1-2 hours. If you intend to keep the application running longer than that, please register for an ngrok account, and connect your account to the ngrok agent. More instructions could be found here: https://dashboard.ngrok.com/get-started/setup). 

The ngrok agent would now show a URL which ends with ’ .eu.ngrok.io’.

Then, in the .env file in the project, which could be found in “ /frontend”, update the ngrok URL to the ngrok URL showing in your ngrok agent, by changing the value of ‘REACT_APP_NGROK_BASE_URL’. 

Finally, start the server by navigating to “ /backend” and run:

python appRoutes.py

### Client

#### Development:

On a separate console (e.g., open a new Command Prompt Window), ensure it is pointed to the root of the project directory. Navigate to “ /frontend” and run:

npm run start

With the server running and the steps above completed, the app should now be successfully running on http://localhost:3000/. 

#### Production:

To create a build directory with the production build of the app, navigate to “ /frontend”, and run: 

npm run build

The application can be deployed on Vercel by first pushing the existing repo code to your GitHub account and linking the GitHub account to your Vercel account. 

Set up the deployment according to the instructions here: https://vercel.com/docs/concepts/get-started/deploy#import-an-existing-project. 
The set-up process should not take more than 10 minutes. 

**Please ensure the .env file has the updated ngrok url which is running, and the server has been started up as well.**

The app should now be successfully running on your Vercel domain. 

(When GitHub project repository is linked to Vercel, if any changes were made to the code, once the changes were committed and pushed to the ‘main’ branch, Vercel would automatically build the application again and deploy it again with the updated changes.)
