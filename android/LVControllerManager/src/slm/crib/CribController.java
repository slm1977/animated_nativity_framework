package slm.crib;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.Switch;
import android.widget.TextView;
import android.os.Build;




public class CribController extends ActionBarActivity {
	
	private static String TAG = "CribController";
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_crib_controller);
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.crib_controller, menu);
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

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment {

    	
    	  TextView txtInfo = null;
    	  
        public PlaceholderFragment() {
        }
        
        
        public void sendRemoteCmd(String cmd)
        {
        	//String url = "http://192.168.1.80:8000/crib/snow_on/";
        	String url = "http://192.168.1.80:8000/crib/" + cmd;
            this.txtInfo.setText("Request:" + url);
            Log.d(TAG, "sending command:"+ cmd);
         // Instantiate the RequestQueue.
            RequestQueue queue = Volley.newRequestQueue(getActivity());

            // Request a string response from the provided URL.
            @SuppressWarnings({ "rawtypes", "unchecked" })
			StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                        new Response.Listener() {
            	

				@Override
				public void onResponse(Object response) {
					txtInfo.setText("Response is: "+  ((String)response));
					
				}
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                      txtInfo.setText("That didn't work:" + error.getMessage());
                }


            });
            // Add the request to the RequestQueue.
            queue.add(stringRequest);

        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_crib_controller, container, false);
            
            Button reqButton = (Button) rootView.findViewById(R.id.button_ok);
            this.txtInfo = (TextView) rootView.findViewById(R.id.txtInfo);
            
            Switch snowSwitch =  (Switch) rootView.findViewById(R.id.switchSnow);
            snowSwitch.setChecked(false);
            //attach a listener to check for changes in state
            snowSwitch.setOnCheckedChangeListener(new OnCheckedChangeListener(){

				@Override
				public void onCheckedChanged(CompoundButton buttonView,
						boolean isChecked) {
					if (isChecked) sendRemoteCmd("snow_on");
					else sendRemoteCmd("snow_off");
					
				}
				});
            
            Switch cloudsSwitch =  (Switch) rootView.findViewById(R.id.switchClouds);
            cloudsSwitch.setChecked(false);
            //attach a listener to check for changes in state
            cloudsSwitch.setOnCheckedChangeListener(new OnCheckedChangeListener(){

				@Override
				public void onCheckedChanged(CompoundButton buttonView,
						boolean isChecked) {
					if (isChecked) sendRemoteCmd("clouds_on");
					else sendRemoteCmd("clouds_off");
					
				}
				});
            
            SeekBar snowBar = (SeekBar)rootView.findViewById(R.id.snow_balls_bar);
            
            snowBar.setOnSeekBarChangeListener(new OnSeekBarChangeListener(){

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
					int value = seekBar.getProgress();
					String cmd = "snow_balls_set_count/" + String.valueOf(value)+"/";
					
					sendRemoteCmd(cmd);
				}});
            
            reqButton.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
                    //doTestRequest();					
				}
			});
            return rootView;
        }
    }
}
