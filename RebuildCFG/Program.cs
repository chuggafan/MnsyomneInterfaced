using System;
using System.IO;
using System.Diagnostics;

namespace RebuildCFG
{
    class Program
    {
        static void Main(string[] args)
        {
            string path = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            path = path.Remove(path.Length - 21);
            path += @"\mnemosyne";
            Console.WriteLine(path);
            Console.ReadKey();
            if (!File.Exists(path + @"\mnemosyne.cfg"))
            {
                Console.WriteLine("Input the username for your archive bot");
                string username = Console.ReadLine();
                Console.WriteLine("Every time you use this bot input the password, this is done at a later step, saving to config files is stupid as hell");
                File.WriteAllText(path + @"\mnemosyne.cfg", @"
[Bot]
useragent: Mnemosyne Reborn by / u / ITSigno
username: " + username +@"
password:

[Reddit]
request_limit: 25
subreddit: kotakuinaction

[Config]
submit_url: http://archive.is/submit/
sleep_time: 60
");
            }
            run_cmd(path + @"\mnemosyne.py");
            Console.ReadKey();
        }
        private static void run_cmd(string cmd)
        {
            string python = @"C:\Python27\python.exe";
            ProcessStartInfo info = new ProcessStartInfo(python);
            info.UseShellExecute = false;
            info.RedirectStandardOutput = true;
            info.Arguments = "\"" + cmd + "\"";
            Process myProcess = new Process();
            myProcess.StartInfo = info;
            myProcess.Start();
            StreamReader myStreamReader = myProcess.StandardOutput;
            string myString = myStreamReader.ReadLine();
            myProcess.WaitForExit();
            myProcess.Close();
        }
    }
}
