package slm.anf.bluetoothtest;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.TooManyListenersException;

import slm.anf.bluetoothtest.ConnectThread.BT_Sender;

import com.javacodegeeks.android.bluetoothtest.R;

import android.app.Activity;
import android.content.res.AssetManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.Toast;
import android.widget.ToggleButton;

public class BT_ControllerActivity extends Activity {
	 public static final String TAG = "BT_ControllerActivity";
	private BT_Sender btSender = null;
	private HashMap<Integer, Integer> pwmMapper = new HashMap<Integer,Integer>();
	
	 private class DigitalPinManager implements OnClickListener, OnSeekBarChangeListener {
       
		 private Properties pinMapperProps = null;
		 
		 private boolean invertedLogic = true;
		 
		 public DigitalPinManager(Properties pinMapperProperties)
		 {
			 this.pinMapperProps = pinMapperProperties;
			this.setupPWM_Mapper();
		 }
		 
		 private void setupPWM_Mapper()
		 {   
			 Enumeration<Object> keyElements = this.pinMapperProps.keys();
			 while(keyElements.hasMoreElements())
			 {
				
				 int[] ids = getButtonPinAndSeekBarId((String)keyElements.nextElement());
				 Log.d(TAG,"Found key id:" + ids[0]);
				 if (ids[1]>0)
				 {
					 pwmMapper.put(ids[1], ids[0]);
				 }
			 }
			   
			 

		 }
		 
		 public void setDigitalPinValue(int pinNumber, boolean pinHIGH)
		 {  
			 if (invertedLogic)
			 {
				 pinHIGH = ! pinHIGH;
			 }
			 String cmd = String.format("D%d,%d|", pinNumber, (pinHIGH ? 1:0) );
			 btSender.sendMessage(cmd);
		 }
		 
		 public void setDigitalPinValue(int pinNumber, int pinValue)
		 {
			 if (pinValue<0) pinValue = 0;
			 else if(pinValue>255) pinValue = 255;
			 
			 if (invertedLogic)
			 {
				 pinValue = 255 - pinValue;
			 }
			 
			 String cmd = String.format("A%d,%d|", pinNumber, pinValue);
			 btSender.sendMessage(cmd);
		 }
		 
		 public int [] getButtonPinAndSeekBarId(String butName)
		 {
			 int [] butInfo = {-1,-1};
			 String info = pinMapperProps.getProperty(butName);
			 if (info!=null)
			 {
				 String [] splitInfo = info.split(",");
				 if (splitInfo.length==1)
				 {
					 butInfo[0] = Integer.parseInt(splitInfo[0]);
				 }
				 else if (splitInfo.length>1)
				 {
					 butInfo[0] = Integer.parseInt(splitInfo[0]);
					 butInfo[1] = getResources().getIdentifier(splitInfo[1], "id", getPackageName()); 
				 }
			 }
			 
			 return butInfo;
		 }
		@Override
		public void onClick(View v) {
			ToggleButton selBut = (ToggleButton) v;
			
			 int butId = selBut.getId();
			 String butName = getResources().getResourceEntryName(butId);
			 Log.d(TAG,"Clicked but:" + butName);
			 int [] ids = getButtonPinAndSeekBarId(butName);
			 if (ids[0]>0)
			 {
				 Toast.makeText(BT_ControllerActivity.this, "Pressed button:" + butName + 
						 " mapped on Pin:" + ids[0] + " seekbar:" + ids[1], Toast.LENGTH_LONG).show();
				 
				 if (ids[1]>0)
				 {
					 SeekBar sb = (SeekBar) findViewById(ids[1]);
					 sb.setEnabled(selBut.isChecked());
					 if (selBut.isChecked())
					 {
						 setDigitalPinValue(ids[0], sb.getProgress());
					 }
					 else
						 setDigitalPinValue( ids[0],false);
				 }
				 else
				 {
					 setDigitalPinValue( ids[0],selBut.isChecked());
				 }
			 }
			 else
			 {
				 Toast.makeText(BT_ControllerActivity.this, "No button mapped found for:" + butName , Toast.LENGTH_LONG).show();
			 }
			 
				 
			 }

		@Override
		public void onProgressChanged(SeekBar seekBar, int progress,
				boolean fromUser) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void onStartTrackingTouch(SeekBar seekBar) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void onStopTrackingTouch(SeekBar seekBar) {
			
        
          if (pwmMapper.containsKey(seekBar.getId()))
        		  {
        	  		int value = seekBar.getProgress();
        	  		int pin = pwmMapper.get(seekBar.getId());
        	  		
        	  		Toast.makeText(BT_ControllerActivity.this,"Sending cmd to pin" + pin + " to value:" + value, Toast.LENGTH_LONG).show();
        		    setDigitalPinValue(pin, value);
        		  }
			
		};
		}

	 private  DigitalPinManager digitalPinListener  = null;
	 
	  private Properties getProperties(String FileName) {
			Properties properties = new Properties();
	        try {
	               /**
	                * getAssets() Return an AssetManager instance for your
	                * application's package. AssetManager Provides access to an
	                * application's raw asset files;
	                */
	               AssetManager assetManager = this.getAssets();
	               /**
	                * Open an asset using ACCESS_STREAMING mode. This
	                */
	               InputStream inputStream = assetManager.open(FileName);
	               /**
	                * Loads properties from the specified InputStream,
	                */
	               properties.load(inputStream);

	        } catch (IOException e) {
	               // TODO Auto-generated catch block
	               Log.e("AssetsPropertyReader",e.toString());
	        }
	        return properties;

	 }

	 
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_bt__controller);
		
		 
		
		this.btSender = (BT_Sender) IntentHelper.getObjectForKey(MainActivity.BT_SENDER_KEY);
		Button butCmd = (Button)findViewById(R.id.butCmd);
	     // butCmd.setEnabled(false);
	      
	      butCmd.setOnClickListener(new OnClickListener() {
		
			@Override
			public void onClick(View v) {
				if (btSender!=null)
				{
					EditText txtView = (EditText) findViewById(R.id.txtBtCmd);
					btSender.sendMessage(txtView.getText().toString());
				}
				
			}
		});
	      
	        Properties pinMapperProperties = getProperties("pin_mapper.properties");
			this.digitalPinListener = new DigitalPinManager(pinMapperProperties);
			
	      this.setupDigitalPinButtons();
	      this.setupSeekBars();
	        
	}
 
	private void setupDigitalPinButtons()
	{
		
		View rootView = findViewById(R.id.digitalPinsGrid);
		ArrayList<View> digitalPinButtons = new ArrayList<View>();
		rootView.findViewsWithText(digitalPinButtons, "digital_pin", View.FIND_VIEWS_WITH_CONTENT_DESCRIPTION);
		
		for (View v : digitalPinButtons)
		{
			v.setOnClickListener(this.digitalPinListener);
			}
	}
	
	private void setupSeekBars()
	{
		View rootView = findViewById(R.id.pwmGrid);
		ArrayList<View> pwm_seekbars = new ArrayList<View>();
		rootView.findViewsWithText(pwm_seekbars , "pwm_seek", View.FIND_VIEWS_WITH_CONTENT_DESCRIPTION);
		
		for (View sb : pwm_seekbars)
		{
			((SeekBar)sb).setOnSeekBarChangeListener(this.digitalPinListener);
		}
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.bt__controller, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
}
