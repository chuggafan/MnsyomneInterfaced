using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
namespace RebuildCFG
{
    class Program
    {
        static void Main(string[] args)
        {
            string path = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            path.Substring(path.Length - 20);
            path += "mnemosyne";
            if (!File.Exists(path + @"\mnemosyne.cfg"))
            {
                File.WriteAllText(@".\mnemosyne.cfg", @"
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
        }
    }
}
