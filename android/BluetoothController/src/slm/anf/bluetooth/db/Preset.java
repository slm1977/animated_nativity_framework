package slm.anf.bluetooth.db;

public class Preset {
  
	private String name;
	private String cmd;

	public Preset(String name, String cmd)
	{
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
	
	@Override
	public String toString()
	{
		return this.name;
	}
}
