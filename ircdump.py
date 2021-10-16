import sys
import pathlib
import socket
import ssl
import random
import textwrap


def main():
    channel = sys.argv[1]
    dumpfile = pathlib.Path(__file__).parent.joinpath(f'{channel}.txt')
    connect_and_dump_loop(dumpfile, channel)


def ssl_socket(server, port):
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock = context.wrap_socket(sock)
    ssock.connect((server, port))
    return ssock


def connect_and_dump_loop(dumpfile, channel, server='irc.chat.twitch.tv', port=6697):
    name_postfix = ''.join([str(i) for i in random.sample(range(0, 9), 3)])
    USERNAME = f'justinfan{name_postfix}'
    PASSWORD = 'kappa'
    comments = []
    
    if not channel.startswith('#'):
        channel = '#' + channel

    conn = ssl_socket(server, port)
    send_cmd(conn, 'NICK', USERNAME)
    send_cmd(conn, 'PASS', PASSWORD)
    send_cmd(conn, 'JOIN', channel)
    
    while True:
        resp = parsemsg( conn.recv(1024).decode('utf-8') )
        if not resp:
            continue
        (prefix, command, args) = resp

        if command == 'PING':
            send_cmd(conn, 'PONG', ':' + ''.join(args))
        elif command == 'PRIVMSG':
            user = prefix.split('!')[0]
            msg_color = '{:06x}'.format( hash(user) % 16777216 )
            msg_text = '\n'.join( textwrap.wrap(args[1].strip(), width=40) )
            msg_line = f'<font color="#{msg_color}">{user}</font>: {msg_text}'
            comments = comments[-9:] + [msg_line]
            comments_str = '\n'.join(comments)
            subtitle = f'1\n0:0:0,0 --> 999:0:0,0\n{comments_str}\n'
            with open(dumpfile, 'w', encoding='utf-8') as f:
                f.write(f'{subtitle}\n')


def send_cmd(conn, cmd, message):
    command = '{} {}\r\n'.format(cmd, message).encode('utf-8')
    print(f'>> {command}')
    conn.send(command)


# https://stackoverflow.com/a/930706
def parsemsg(s):
    prefix = ''
    trailing = []
    if not s:
        return None
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args


if __name__ == '__main__':
    main()
