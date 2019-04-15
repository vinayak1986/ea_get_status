The script is used to fetch the status of the CDR application submitted to Engineers Australia from their portal. We use the *requests* library to first execute a POST call to the site using the required parameters. This is followed by a GET call on the application home page to get the status.

Apr 15, 2019
Added logic to send SMS if the status changes from 'Queued for assessment'. Also, the POST call will now try to execute 5 times if an error code is thrown.

