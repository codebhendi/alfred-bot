import imaplib
import email
import re
from dateutil import parser

# pop_conn = poplib.POP3_SSL('pop.gmail.com')
# pop_conn.user('bhendarkar.shubham')
# pop_conn.pass_('nagpur9182')
# #Get messages from server:
# #messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# messages = pop_conn.retr(1)
# message = "\n".join(messages[1])
# # Concat message pieces:
# #messages = ["\n".join(mssg[1]) for mssg in messages]
# #Parse message intom an email object:
# messages = parser.Parser().parsestr(message)
# #for message in messages:
# #    print message['subject']
# #pop_conn.quit()
# print(messages)
def getSender(email):
    """
        Returns the best-guess sender of an email.

        Arguments:
        email -- the email whose sender is desired

        Returns:
        Sender of the email.
    """
    sender = email['From']
    m = re.match(r'(.*)\s<.*>', sender)
    if m:
        return m.group(1)
    return sender

def getDate(email):
    return parser.parse(email.get('date'))

def fetchUnreadEmails(since=None, markRead=False, limit=None):
    """
        Fetches a list of unread email objects from a user's Gmail inbox.

        Arguments:
        profile -- contains information related to the user (e.g., Gmail
                   address)
        since -- if provided, no emails before this date will be returned
        markRead -- if True, marks all returned emails as read in target inbox

        Returns:
        A list of unread email objects.
    """
    conn = imaplib.IMAP4_SSL('imap.gmail.com')
    conn.debug = 0
    conn.login("bhendarkar.shubham", "nagpur9182")
    conn.select(readonly=(not markRead))

    msgs = []
    (retcode, messages) = conn.search(None, '(UNSEEN)')

    if retcode == 'OK' and messages != ['']:
        numUnread = len(messages[0].split(' '))

        print(limit)
        if limit and numUnread > limit:
            return numUnread

        for num in messages[0].split(' '):
            # parse email RFC822 format
            ret, data = conn.fetch(num, '(RFC822)')
            msg = email.message_from_string(data[0][1])

            if not since or getDate(msg) > since:
                msgs.append(msg)
    conn.close()
    conn.logout()

    return msgs

    def check_command(speaker, data):
        if not ("check" in data) :
            return
        try:
            msgs = fetchUnreadEmails(profile, limit=5)

            if isinstance(msgs, int):
                response = "You have %d unread emails." % msgs
                speaker.say(response)
                return

            senders = [getSender(e) for e in msgs]
        except imaplib.IMAP4.error:
            speaker.say(
                "I'm sorry. I'm not authenticated to work with your Gmail.")
            return

        if not senders:
            speaker.say("You have no unread emails.")
        elif len(senders) == 1:
            spekaer.say("You have one unread email from " + senders[0] + ".")
        else:
            response = "You have %d unread emails" % len(
                senders)
            unique_senders = list(set(senders))
            if len(unique_senders) > 1:
                unique_senders[-1] = 'and ' + unique_senders[-1]
                response += ". Senders include: "
                response += '...'.join(senders)
            else:
                response += " from " + unique_senders[0]

            speaker.say(response)