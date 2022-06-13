class ListHelper:
    @staticmethod
    def split(masterList, n):
        k, m = divmod(len(masterList), n)
        return (masterList[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
