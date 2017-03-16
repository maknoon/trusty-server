```
  ______ _ __  _    __  ()    ______ _    ,
    /   ' )  )' )  /    /\      /   ' )  / 
 --/     /--'  /  /    /  )  --/     /  /  
(_/     /  \_ (__/    /__/__(_/     (__/_  
                                     //    
                                    (/     
                                    v0.0.1
~ (PROVISIONAL COPY OF) The TrustyCompanion & TrustyTracker's Trusty Backend Application ~
```

#### Environment Requirements (Ubuntu-optimized):  
* [Python 2.7+](https://www.python.org/)  
* [pip](https://pypi.python.org/pypi/pip)  
* [Flask](http://flask.pocoo.org/)  
* [Apache](https://httpd.apache.org/) + Apache2 WSGI Module  
* [MySQL](https://www.mysql.com/)  


#### Development:  
The trusty-server is up and running on our own Amazon EC2 instance. To access the server via secure shell, do the following:  
1. Store the cpen391.pem key from our secure GoogleDrive to your local `.ssh` folder  
2. In your `.ssh/config` file (create if does not exist), copy in:
```
Host trusty
	Hostname x.x.x.x
	User ubuntu
	IdentityFile ~/.ssh/cpen391.pem
```
Now you can access server from your commandline by using `$ ssh trusty`  


#### Other Information:  
1. The live hostname is: [omitted] (also accessible at x.x.x.x), which may change if the instance is ever re-deployed.  
2. The Apache server is constantly running a compiled version of the Flask app from `/var/www/html/trusty-server`, which has been symbolically linked to `~/trusty-server`.  


#### Testing on the live server:  
1. Clone this repository, and make your desired changes.  
2. Navigate to the parent directory of this repository and execute `$ rsync -av --exclude 'trusty-server/res/exclude.txt' /path/to/your/local/trusty-server trusty:trusty-server`  
3. ssh into the instance (see above)  
4. Execute `$ sudo apachectl restart` and restart your ssh connection; the server will then restart and you should be able to see changes by navigating to the live hostname.
