package slm.anf.bluetooth.db;


import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;

public class DbAdapter {
  @SuppressWarnings("unused")
  private static final String LOG_TAG = DbAdapter.class.getSimpleName();
         
  private Context context;
  private SQLiteDatabase database;
  private DatabaseHelper dbHelper;
 
  // Database fields
  private static final String DATABASE_TABLE      = "presets";
 
  public static final String KEY_PRESETSID = "_id";
  public static final String KEY_NAME = "name";
  public static final String KEY_CMD = "cmd";

  public DbAdapter(Context context) {
    this.context = context;
  }
 
  public DbAdapter open() throws SQLException {
    dbHelper = new DatabaseHelper(context);
    database = dbHelper.getWritableDatabase();
    return this;
  }
 
  public void close() {
    dbHelper.close();
  }
 
  private ContentValues createContentValues(String name, String cmd ) {
    ContentValues values = new ContentValues();
    values.put( KEY_NAME,  name);
    values.put( KEY_CMD,  cmd );
    
   return values;
  }
         
  //create a preset
  public long createPreset(String name, String cmd ) {
    ContentValues initialValues = createContentValues(name, cmd);
    return database.insertOrThrow(DATABASE_TABLE, null, initialValues);
  }
 
  //update a preset
  public boolean updatePreset( long presetID, String name, String cmd) {
    ContentValues updateValues = createContentValues(name, cmd);
    return database.update(DATABASE_TABLE, updateValues, KEY_PRESETSID + "=" + presetID, null) > 0;
  }
                 
  //delete a preset    
  public boolean deletePreset(long presetID) {
    return database.delete(DATABASE_TABLE, KEY_PRESETSID + "=" + presetID, null) > 0;
  }
 
  //fetch all presets
  public Cursor fetchAllPresets() {
    return database.query(DATABASE_TABLE, new String[] { KEY_PRESETSID, KEY_NAME, KEY_CMD}, null, null, null, null, null);
  }
   
 
  public Cursor fetchPreset( long contactID ) throws SQLException {
      
      Cursor mCursor = database.query(true, DATABASE_TABLE, new String[] {
               KEY_PRESETSID, KEY_NAME, KEY_CMD
              },
              KEY_PRESETSID + "=" + contactID, null, null, null, null, null);
       
      return mCursor;
  } 
  //fetch contacts filter by a string
  public Cursor fetchPresetsByFilter(String filter) {
    Cursor mCursor = database.query(true, DATABASE_TABLE, new String[] {
                                    KEY_PRESETSID, KEY_NAME, KEY_CMD},
                                    KEY_NAME + " like '%"+ filter + "%'", null, null, null, null, null);
         
    return mCursor;
  }
  
}