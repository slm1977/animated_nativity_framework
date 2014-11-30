package slm.anf.anf_bt_connector;


import android.bluetooth.*;

public class BTConnector {
    String status = "N.A";
    
	public BTConnector(){
	BluetoothAdapter bluetooth = BluetoothAdapter.getDefaultAdapter();
	
	if(bluetooth != null)
	{
		if (bluetooth.isEnabled()) {
			String mydeviceaddress = bluetooth.getAddress();
		    String mydevicename = bluetooth.getName();
		    status = mydevicename + ” : ” + mydeviceaddress;
		}
		else
		{
			
		}
	}
	
	}
}
