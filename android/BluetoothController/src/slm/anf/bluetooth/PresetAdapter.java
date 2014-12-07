package slm.anf.bluetooth;

/*
 * Project MOST - Moving Outcomes to Standard Telemedicine Practice
 * http://most.crs4.it/
 *
 * Copyright 2014, CRS4 srl. (http://www.crs4.it/)
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * See license-GPLv2.txt or license-MIT.txt
 */



import java.util.List;
import com.javacodegeeks.android.bluetoothtest.R;
import slm.anf.bluetooth.db.Preset;



import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;


class PresetAdapter extends ArrayAdapter<Preset> {
   
	private List<Preset> presets = null;
	
	/**
	 * This adapter provides a way of rendering informations about a list of {@link IStream} objects.
	 * @param context
	 * @param viewId the view id where to render the informations about each stream
	 * @param objects the list of {@link IStream} objects.
	 * @param streamProperties the properties to render for each stream (a null value renders all the available properties)
	 */
    public PresetAdapter(Context context, int viewId,
                 List<Preset> presets) {
        super(context, viewId, presets);
        this.presets = presets;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        return getViewOptimize(position, convertView, parent);
    }

    private View getViewOptimize(int position, View convertView, ViewGroup parent) {
        ViewHolder viewHolder = null;
        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) getContext()
                      .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.preset_row, null);
            viewHolder = new ViewHolder();
            viewHolder.name = (TextView)convertView.findViewById(R.id.txtPresetName);
            viewHolder.name.setText(presets.get(position).getName());
            
            convertView.setTag(viewHolder);
        } else {
            viewHolder = (ViewHolder) convertView.getTag();
        }
        
     
        return convertView;
    }
   
    private class ViewHolder {
        public TextView name;
      
    }
}
