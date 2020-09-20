from goa import GOA
from evidence import Evidence

class Instance:
    """
    Define GOA-Evidence Instance class
    A GOA-Evidence Instance contain evidence info and GOA info

    """
    def __init__(self):
        self.annotation_id = "#annotation_id"
        self.evidence = Evidence()
        self.goa = GOA()

    def tostring(self):
        """
        This method will convert an GOA-evidence instance object to string object

        :return: a string
        """
        goa = self.goa.tostring() # convert goa info to string
        evidence = self.evidence.tostring() # convert evidence info to string

        s = '|'.join((self.annotation_id,
                     evidence,
                     goa))

        s += '\n' # add a line breaker
        return s

    def fromstring(self, s):
        """
        This method will convert an string to an instance object
        :param instance:
        :return:
        """
        instance = Instance()
        template = s.strip('\n').split('|')
        instance.annotation_id = template[0]
        evidence = '|'.join(template[1:7]) # evidence part
        goa = '|'.join(template[7:]) # goa part

        instance.evidence = Evidence().fromstring(evidence)
        instance.goa = GOA().fromstring(goa)
        return instance

    def save_instance_to_txt(self,instance,file_path,appending):
        """
        This method will convert an instance to string and save to txt file

        :param instance: Instance object
        :param file_path: file storage path
        :param appending: False for rewriting the file;
                          True for appending the new string to the file
        :return: FileIO
        """
        s = self.tostring()
        instance.save_string_to_txt(s, file_path,appending)

    def save_string_to_txt(self, s, file_path, appending):
        if appending:
            with open(file_path,'a',encoding='utf-8') as wf:
                wf.write(s)
            wf.close()
        else:
            with open(file_path,'w',encoding='utf-8') as wf:
                wf.write(s)
            wf.close()
        print("string written to file {} complete".format(file_path))


if __name__ == '__main__':
    instance = Instance()
    s = instance.tostring()
    print(s)
    i = Instance().fromstring(s)
    print(i.tostring())




