"""
Generates list of current authors
Run the script in the main sympy repo.
Copy authors.tex in the tutorial repo.
"""


def generate_authors_list():
    authors = []
    with open('AUTHORS') as f:
        for line in f:
            if line.strip().endswith('>'):
                aut = line.split('<')[0].strip() + '\\\\' + '\n'
                if aut.startswith('*'):
                    aut = aut[1:]
                authors.append(aut)
    return authors


def generate_authors_tex(authors, batch=100):
    begin_frame1 = '\\begin{frame}{Authors}\n'
    begin_frame2 = '\\begin{frame}{Authors (continued)}\n'
    end_frame = '\\end{frame}\n'
    begin_multicols = '\\begin{multicols}{5}\n'
    end_multicols = '\\end{multicols}\n'
    tiny = '\\tiny\n'
    with open('authors.tex', 'w') as f:
        for i in range(0, len(authors), batch):
            if i:
                f.write(begin_frame2)
            else:
                f.write(begin_frame1)
            f.write(begin_multicols)
            f.write(tiny)
            if(i + batch < len(authors)):
                end = i + batch
            else:
                end = len(authors)
            authors_text = ''.join(authors[i:end])
            f.write(authors_text)
            f.write(end_multicols)
            f.write(end_frame)


if __name__ == '__main__':
    authors = generate_authors_list()
    generate_authors_tex(authors, 110)
