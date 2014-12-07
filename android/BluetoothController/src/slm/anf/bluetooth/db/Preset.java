package slm.anf.bluetooth.db;

public class Preset {
  
	private int id;
	private String name;
	private String cmd;

	public Preset(int id, String name, String cmd)
	{
		this.id = id;
		this.name = name;
		this.cmd = cmd;
	}
	
	public String getName()
	{
		return this.name;
	}
	
	public String getCommand()
	{
		return this.cmd;
	}
	
	public int getId()
	{
		return this.id;
	}
	
	@Override
	public String toString()
	{
		return this.name;
	}
}
