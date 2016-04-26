using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
                File.WriteAllText(path + @"\mnemosyne.cfg", @"
[Bot]
useragent: Mnemosyne Reborn by / u / ITSigno
username: mnemosyne - 0001
password:

[Reddit]
request_limit: 25
subreddit: kotakuinaction

[Config]
submit_url: http://archive.is/submit/
sleep_time: 60
exclude: archive\.is, youtube\.com, web\.archive\.org

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
            info.Arguments = cmd;
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
