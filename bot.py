import socket, re, subprocess, os, time, threading, sys, re, requests
       
server = "192.186.157.43"
channel = "##pihui"
botnick = "youtubeBot"

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n")
ircsock.send("NICK "+ botnick +"\n")

def ping(): # respond to server Pings.
  ircsock.send("PONG :pingis\n")  

def sendmsg(msg): # sends messages to the channel.
  ircsock.send("PRIVMSG "+ channel +" :"+ msg +"\n") 

def youtubeSearch(request):
  r = requests.get('https://www.youtube.com/results', params={'search_query': request})
  v = re.search(r'/watch\?v=([\w-]*)', r.text)
  sendmsg('https://www.youtube.com' + v.group())

def youtubeEmptySearch():
  r = requests.get('https://www.youtube.com/')
  v = re.search(r'/watch\?v=([\w-]*)', r.text)
  sendmsg('https://www.youtube.com' + v.group())

def emptyinput():
  sendmsg("Usage:")
  sendmsg("youtubeBot: do some magic <your search request on YouTube>")
  sendmsg("Random video from \"On trending\" for you:")
  youtubeEmptySearch()

def main():
  ircsock.send("JOIN "+ channel +"\n")

  with open("ircchat.log", "w") as temp:
    temp.write("")
    
  while 1: 
    # clear ircmsg value every time
    ircmsg = ""
    # set ircmsg to new data received from server
    ircmsg = ircsock.recv(2048)
    # remove any line breaks
    ircmsg = ircmsg.strip('\n\r') 
    # print received message to stdout (mostly for debugging).
    #print(ircmsg)

    # repsond to pings so server doesn't think we've disconnected
    if ircmsg.find("PING :") != -1: 
      ping()
      # look for PRIVMSG lines as these are messages in the channel or sent to the bot
    if ircmsg.find("PRIVMSG") != -1:
      name = ircmsg.split('!',1)[0][1:]
      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      print(name+ ": "+ message)

      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      if ircmsg.find("youtubeBot: do some magic") != -1:
        searchWord = message.split('youtubeBot: do some magic', 1)[1][1:]
        if (searchWord == ''):
          emptyinput()
        else:
          youtubeSearch(searchWord)
        
main()