package slm.anf.bluetooth;

import android.os.Bundle;
import android.app.Activity;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import java.util.Set;


import slm.anf.bluetooth.ConnectThread.BT_Listener;
import slm.anf.bluetooth.ConnectThread.BT_Sender;

import slm.anf.bt_controller.R;

import android.content.Intent;
import android.content.IntentFilter;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {

   private static final int REQUEST_ENABLE_BT = 1;
   private Button findBtn;
   private TextView text;
   private BluetoothAdapter myBluetoothAdapter;
   private Set<BluetoothDevice> pairedDevices;
   private ListView myListView;
   private ArrayAdapter<String> BTArrayAdapter;
   private BT_Sender btSender = null;
    
   
   public static final String BT_SENDER_KEY = "bt_sender";
   public static final int BT_SENDER_READY = 99999;
   private static final String TAG = "BTMainActivity";
   
   private ProgressDialog searchDevicesProgress = null;
   private ProgressDialog connectToDeviceProgress = null;
   
   @Override
   protected void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      setContentView(R.layout.activity_main);
      
      
      
      // take an instance of BluetoothAdapter - Bluetooth radio
      myBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
      if(myBluetoothAdapter == null) {
    	  findBtn.setEnabled(false);
    	   
    	  
    	  Toast.makeText(getApplicationContext(),"Your device does not support Bluetooth",
         		 Toast.LENGTH_LONG).show();
      } else {
	        
	      findBtn = (Button)findViewById(R.id.search);
	      findBtn.setOnClickListener(new OnClickListener() {
	  		
	  		@Override
	  		public void onClick(View v) {
	  			// TODO Auto-generated method stub
	  			find(v);
	  		}
	      });
	    
	      myListView = (ListView)findViewById(R.id.listView1);
	
	      // create the arrayAdapter that contains the BTDevices, and set it to the ListView
	      BTArrayAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1);
	      myListView.setAdapter(BTArrayAdapter);
	      
	      myListView.setOnItemClickListener(new OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				
				String selDeviceInfo = BTArrayAdapter.getItem(position);
				String deviceName= selDeviceInfo.split("\n")[0];
				String macAddress=  selDeviceInfo.split("\n")[1];
				BluetoothDevice device =  myBluetoothAdapter.getRemoteDevice(macAddress);
				Log.d(TAG,"selected:" + macAddress);
				
				//Toast.makeText(MainActivity.this, "Connecting to:" + deviceName + "(" + macAddress +")" , Toast.LENGTH_LONG).show();
				connectToDeviceProgress = new ProgressDialog(MainActivity.this);
				connectToDeviceProgress.setTitle("Remote Blueetooth Device Connection");
				connectToDeviceProgress.setMessage("Connecting to " + deviceName +". Please wait ...");
				
				connectToDeviceProgress.show();
				
				
				ConnectThread ct = new ConnectThread(device, myBluetoothAdapter, new BT_Listener() {
					
					@Override
					public void onBT_SenderReady(BT_Sender btSender) {
						MainActivity.this.btSender = btSender;	
						IntentHelper.addObjectForKey(btSender, BT_SENDER_KEY);
						 
						Intent btIntent = new Intent(MainActivity.this, BT_ControllerActivity.class);
						connectToDeviceProgress.dismiss();
						startActivity(btIntent);
						
					}
				});
				
			}
		});
	       
	   // Activate BT
  	    on();
	    
      } 
   }

   public void on(){
      if (!myBluetoothAdapter.isEnabled()) {
         Intent turnOnIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
         startActivityForResult(turnOnIntent, REQUEST_ENABLE_BT);

         Toast.makeText(getApplicationContext(),"Bluetooth turned on" ,
        		 Toast.LENGTH_LONG).show();
      }
      else{
         Toast.makeText(getApplicationContext(),"Bluetooth is already on",
        		 Toast.LENGTH_LONG).show();
         if(myBluetoothAdapter.isEnabled()) {
			  
        	 list();
         	}
         else {   
			  Toast.makeText(this, "Bt disabled", Toast.LENGTH_LONG).show();
		   }
          
      }
   }
   
   @Override
   protected void onActivityResult(int requestCode, int resultCode, Intent data) {
	   // TODO Auto-generated method stub
	   if(requestCode == REQUEST_ENABLE_BT){
		   if(myBluetoothAdapter.isEnabled()) {
			 
			   list();
		   } else {   
			  Toast.makeText(this, "Bt disabled", Toast.LENGTH_LONG).show();
		   }
	   }
   }
   
   public void list(){
	  // get paired devices
      pairedDevices = myBluetoothAdapter.getBondedDevices();
      BluetoothDevice selDevice = null;
      
      // put it's one to the adapter
      for(BluetoothDevice device : pairedDevices)
      {
    	  BTArrayAdapter.add(device.getName()+ "\n" + device.getAddress());
    	  selDevice = device;
      }
      
      //Toast.makeText(getApplicationContext(),"Show Paired Devices. Sending command!",  Toast.LENGTH_SHORT).show();
      
   }
   
   final BroadcastReceiver bReceiver = new BroadcastReceiver() {
	    public void onReceive(Context context, Intent intent) {
	    	
	    	if (searchDevicesProgress!=null)
	    		searchDevicesProgress.dismiss();
	    	
	        String action = intent.getAction();
	        // When discovery finds a device
	        if (BluetoothDevice.ACTION_FOUND.equals(action)) {
	             // Get the BluetoothDevice object from the Intent
	        	 BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
	        	 // add the name and the MAC address of the object to the arrayAdapter
	             BTArrayAdapter.add(device.getName() + "\n" + device.getAddress());
	             BTArrayAdapter.notifyDataSetChanged();
	        }
	    }
	};
	
   public void find(View view) {
	   if (myBluetoothAdapter.isDiscovering()) {
		   // the button is pressed when it discovers, so cancel the discovery
		   myBluetoothAdapter.cancelDiscovery();
	   }
	   else {
			BTArrayAdapter.clear();
			
			searchDevicesProgress = new ProgressDialog(this);
			searchDevicesProgress.setTitle("Searching for bluetooth devices");
			searchDevicesProgress.setMessage("Please wait while searching...");
			searchDevicesProgress.show();
			
			myBluetoothAdapter.startDiscovery();
			
			registerReceiver(bReceiver, new IntentFilter(BluetoothDevice.ACTION_FOUND));	
		}    
   }
   
   public void off(){
	  myBluetoothAdapter.disable();
	  text.setText("Status: Disconnected");
	  
      Toast.makeText(getApplicationContext(),"Bluetooth turned off",
    		  Toast.LENGTH_LONG).show();
   }
   
   @Override
   protected void onDestroy() {
	   // TODO Auto-generated method stub
	   super.onDestroy();
	   try{
	   unregisterReceiver(bReceiver);
	   } catch(Exception ex)
	   {
		   Log.d(TAG,"Receiver unregistration ignored");
	   }
   }
		
}
