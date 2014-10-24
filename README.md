API

Base path: http://api.olidu.com 


<table>
<tr> <td> Category</td><td>Path</td><td>Method</td><td>Description</td></tr>
<tr><td>User</td> <td>/sq/enqueue/user_id/queue_id</td><td> put </td><td>Take a position in queue</td> </tr>
<tr><td>User</td> <td>/sq/queue/queue_id/reservation_id </td><td> get </td><td>Query the status of a queue regarding to a particular reservation</td> </tr>
<tr><td>Vendor</td> <td>/sq/dequeue/queue_id/reservation_id </td><td> post </td><td>Mark the reservation has been called/served</td> </tr>


</table>

For example http://api.olidu.com/sq/enqueue/1/1  



Use Chrome app "REST Console" to test it. 
