def validate_note(content: str)->str:
    i=0
    j=len(content)-1
    while i<len(content):
        if content[i]!=" " and content[i]!="\t" and content[i]!="\n":
            break
        i+=1
    while j>=0:
        if content[j]!=" " and content[j]!="\t" and content[j]!="\n":
            break
        j-=1
    if i>j:
        return ""
    return content[i:j+1] # 注意切片规则