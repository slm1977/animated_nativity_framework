package slm.anf.bluetooth;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;
import java.util.Set;
import java.util.TooManyListenersException;


import slm.anf.bluetooth.ConnectThread.BT_Sender;
import slm.anf.bluetooth.db.DbAdapter;
import slm.anf.bluetooth.db.Preset;

import slm.anf.bt_controller.R;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.content.res.AssetManager;
import android.database.Cursor;
import android.os.Bundle;
import android.text.Editable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.AdapterView.OnItemLongClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.Toast;
import android.widget.ToggleButton;

public class BT_ControllerActivity extends Activity {
	public static final String TAG = "BT_ControllerActivity";
	
	private BT_Sender btSender = null;
	private HashMap<Integer, Integer> pwmMapper = new HashMap<Integer,Integer>();
	private DbAdapter dbHelper = null;
	private PresetAdapter presetAdapter = null;
	
    private class DigitalPinManager implements OnClickListener, OnSeekBarChangeListener {
       
		 private Properties pinMapperProps = null;
		 private boolean invertedLogic = false;
		 private HashMap<Integer, String>  cmdMapper = new HashMap<Integer, String>(); // Key: Pin; Value: Command
		 private HashMap<Integer, String>  pinMapper = new HashMap<Integer, String>(); // Key Pin; Value: ButtonName
		 
		 public String getCommandPreset()
		 {
			 StringBuffer cmd = new StringBuffer();
			 Set<Integer> keys = this.cmdMapper.keySet();
			   
			 
			 for (int k: keys)
				 cmd.append(this.cmdMapper.get(k));
		 
			 return cmd.toString();
		 }
		 
		 public DigitalPinManager(Properties pinMapperProperties)
		 {
			this.pinMapperProps = pinMapperProperties;
			this.setupMappers();
		 }
		 
		 private void setupMappers()
		 {   
			 Enumeration<Object> keyElements = this.pinMapperProps.keys();
			 while(keyElements.hasMoreElements())
			 {
				 String butName = (String)keyElements.nextElement();
				 int[] ids = getButtonPinAndSeekBarId(butName);
				 Log.d(TAG,"Found key id:" + ids[0]);
				 pinMapper.put( ids[0], butName);
				 if (ids[1]>0)
				 {
					 // Key: seekBarId. Value: Pin Number
					 pwmMapper.put(ids[1], ids[0]);
				 }
				 // inizialize all pins to the LOW value
				 setDigitalPinValue(ids[0],false,true);
			 }
			   
		 }
		 
		 public String setDigitalPinValue(int pinNumber,boolean pinHIGH)
		 {
			 return setDigitalPinValue(pinNumber, pinHIGH, true);
		 }
		 
		 public String setDigitalPinValue(int pinNumber, boolean pinHIGH, boolean sendCmd)
		 {  
			 if (invertedLogic)
			 {
				 pinHIGH = ! pinHIGH;
			 }
			 String cmd = String.format("D%d,%d|", pinNumber, (pinHIGH ? 1:0) );
			 this.cmdMapper.put(pinNumber, cmd);
			 if (sendCmd) {
				 btSender.sendMessage(cmd);
			 }
			 return cmd;
		 }
		 
		 public String setDigitalPinValue(int pinNumber, int pinValue)
		 {
			 return setDigitalPinValue(pinNumber,  pinValue, true);
		 }
				 
		 public String setDigitalPinValue(int pinNumber, int pinValue, boolean sendCmd)
		 {
			 if (pinValue<0) pinValue = 0;
			 else if(pinValue>255) pinValue = 255;
			 
			 if (invertedLogic)
			 {
				 pinValue = 255 - pinValue;
			 }
			 
			 String cmd = String.format("A%d,%d|", pinNumber, pinValue);
			 this.cmdMapper.put(pinNumber, cmd);
			 if (sendCmd)
			 {
				 btSender.sendMessage(cmd);
			 }
				
			 return cmd;
		 }
		 
		 public void setGUIforCommand(String cmd){
			 
			 String [] cmds = cmd.split("[|]");
			 
			 for (String c : cmds)
			 {
				 boolean isDigital = c.startsWith("D");
				 int pinNumber = Integer.parseInt(c.substring(1, c.indexOf(",")));
				 int pinValue = Integer.parseInt(c.substring(c.indexOf(",")+1));
				 
				 String butName = pinMapper.get(pinNumber);
				 int butId = getResources().getIdentifier(butName, "id", getPackageName()); 
				 
				 ((ToggleButton) findViewById(butId)).setChecked(pinValue>0);
				 
				 int [] ids = getButtonPinAndSeekBarId(butName);
				 if (ids[1]>0)
				 {
					 ((SeekBar) findViewById(ids[1])).setProgress(pinValue);
				 }
			 }
		 }
		/**
		 *Get the Pin number and the seekbar id (or -1 if no provided) associated to the button specified as parameter
		 * @param butName
		 * @return {pin_number, seek_bar_id}
		 */
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
			
			preset_list.clearChoices();
			presetAdapter.notifyDataSetChanged();
			
			ToggleButton selBut = (ToggleButton) v;
			
			 int butId = selBut.getId();
			 String butName = getResources().getResourceEntryName(butId);
			 Log.d(TAG,"Clicked but:" + butName);
			 int [] ids = getButtonPinAndSeekBarId(butName);
			 String cmd = null;
			 if (ids[0]>0)
			 {
				// Toast.makeText(BT_ControllerActivity.this, "Pressed button:" + butName +  " mapped on Pin:" + ids[0] + " seekbar:" + ids[1], Toast.LENGTH_LONG).show();
				 
				 
				 
				 if (ids[1]>0)
				 {
					 SeekBar sb = (SeekBar) findViewById(ids[1]);
					 sb.setEnabled(selBut.isChecked());
					 if (selBut.isChecked())
					 {
						 cmd = setDigitalPinValue(ids[0], sb.getProgress());
					 }
					 else
						 cmd = setDigitalPinValue( ids[0],false);
				 }
				 else
				 {
					 cmd = setDigitalPinValue( ids[0],selBut.isChecked());
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
		
			preset_list.clearChoices();
			presetAdapter.notifyDataSetChanged();
        
          if (pwmMapper.containsKey(seekBar.getId()))
        		  {
        	  		int value = seekBar.getProgress();
        	  		int pin = pwmMapper.get(seekBar.getId());
        	  		
        	  		//Toast.makeText(BT_ControllerActivity.this,"Sending cmd to pin" + pin + " to value:" + value, Toast.LENGTH_LONG).show();
        		    setDigitalPinValue(pin, value);
        		  }
			
		};
		}

    
     private void showPresetEditorDialog(final Preset preset)
     {
    	 final Dialog dialog = new Dialog(this);
			dialog.setContentView(R.layout.preset_editor);
			
			dialog.setTitle("Preset Editor:" + preset.getName());
			final EditText txtName = (EditText) dialog.findViewById(R.id.editName);
			txtName.setText(preset.getName());
			
			final EditText txtCmd = (EditText) dialog.findViewById(R.id.editCommand);
			txtCmd.setText(preset.getCommand());
			Button butCancel = (Button) dialog.findViewById(R.id.button_cancel);
			butCancel.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View v) {
					dialog.dismiss();
				}
			});
			
			Button butSave = (Button) dialog.findViewById(R.id.button_save);
			butSave.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View v) {
					
					 String name = txtName.getText().toString();
					 String cmd = txtCmd.getText().toString();
					 updatePreset(preset, name, cmd);
					dialog.dismiss();
					
				}
			});
			
			Button butDelete = (Button) dialog.findViewById(R.id.button_delete);
			butDelete.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View v) {
					
					deletePreset(preset);
					dialog.dismiss();
					
				}
			});
			
			dialog.show();
     }
	 private  DigitalPinManager digitalPinListener  = null;

	 private ListView preset_list;
	 
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
		
		this.dbHelper = new DbAdapter(this);
		
		
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
	      this.setupPresetsListView();
	}
 
	 
	 
	 /**
     * Function to load the spinner data from SQLite database
     * */
    private void setupPresetsListView() {
        
        // Spinner Drop down elements
        List<Preset> presets = loadAllPresets();
 
        // Creating adapter for spinner
         presetAdapter = new PresetAdapter(this,
                R.layout.preset_row, presets);
 
        // Drop down layout style - list view with radio button
        //resetAdapter
        //        .setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        preset_list = (ListView) findViewById(R.id.preset_list);
      
        
        LayoutInflater inflater = getLayoutInflater();
        
        ViewGroup header = (ViewGroup)inflater.inflate(R.layout.preset_header, preset_list, false);
        
       
        
        preset_list.addHeaderView(header, null, false);
        // attaching data adapter to spinner
        preset_list.setAdapter(presetAdapter);
        
        preset_list.setOnItemLongClickListener(new OnItemLongClickListener() {

			@Override
			public boolean onItemLongClick(AdapterView<?> parent, View view,
					int position, long id) {
				Preset preset = (Preset) parent.getItemAtPosition(position);
				showPresetEditorDialog(preset);
				return false;
			}
		});
        
        preset_list.setOnItemClickListener(new OnItemClickListener() {
 

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				Preset preset = (Preset) parent.getItemAtPosition(position);
				setPreset(preset);
		        
			}

		 
		});
      
    }
    
    private void setPreset(Preset preset)
    {
    	
		//Toast.makeText(BT_ControllerActivity.this, "LOADING CMD:" + preset.getCommand(), Toast.LENGTH_LONG).show();
		btSender.sendMessage(preset.getCommand());
		digitalPinListener.setGUIforCommand(preset.getCommand());
    }
    
    private void refreshPresetList()
    {
    	presetAdapter.clear();
    	presetAdapter.addAll(loadAllPresets());
    	presetAdapter.notifyDataSetChanged();
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
	
	
	private List<Preset>loadAllPresets()
	{   
		ArrayList<Preset> presets = new ArrayList<Preset>();
		dbHelper.open();
		Cursor cursor = dbHelper.fetchAllPresets();
	
		startManagingCursor(cursor);
		 
		 while ( cursor.moveToNext() ) {
		                 
		    String presetName = cursor.getString( cursor.getColumnIndex(DbAdapter.KEY_NAME) );
		    String presetCmd = cursor.getString( cursor.getColumnIndex(DbAdapter.KEY_CMD) );
		    int presetId = cursor.getInt(cursor.getColumnIndex(DbAdapter.KEY_PRESETSID));
		    presets.add(new Preset(presetId,presetName, presetCmd));
		   // Log.d(TAG, "preset name = " + presetName + " CMD:" + presetCmd);  
		 	}
		 dbHelper.close();
		 return presets;
	}
	
	
	private void showSavePresetDialog()
	{
		// Set an EditText view to get user input 
		final EditText input = new EditText(this);

		new AlertDialog.Builder(BT_ControllerActivity.this)
	    .setTitle("Saving Preset")
	    .setMessage("Enter the preset name:")
	    .setView(input)
	    .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
	        public void onClick(DialogInterface dialog, int whichButton) {
	            Editable name = input.getText(); 
	            savePreset(name.toString());
	        }
	    }).setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
	        public void onClick(DialogInterface dialog, int whichButton) {
	            // Do nothing.
	        }
	    }).show();

		
	}
	private void savePreset(String name)
	{
		String cmd = this.digitalPinListener.getCommandPreset();
		//Toast.makeText(this, "Cmd:" + cmd, Toast.LENGTH_LONG).show();
		 dbHelper.open();
		 dbHelper.createPreset(name, cmd);
	     dbHelper.close();
	     
	     // reload the presets in the list view
	     refreshPresetList();
	}
	
	private void deletePreset(Preset preset)
	{
		 dbHelper.open();
		 dbHelper.deletePreset(preset.getId());
		 dbHelper.close();
		 refreshPresetList();
	}
	
	private void updatePreset(Preset preset, String name, String cmd)
	{
		dbHelper.open();
		dbHelper.updatePreset(preset.getId(), name, cmd);
		dbHelper.close();
	    refreshPresetList();
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
		if (id == R.id.mnu_save_as_preset) {
			showSavePresetDialog();
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
}
