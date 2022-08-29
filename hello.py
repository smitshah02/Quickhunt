from flask import Flask, request, render_template
import sports
import india
import tech
import education
import topnews

app = Flask(__name__)

size, art_summary, art_titles, art_sentiments, art_links = sports.passon()
isize,isummary,ititles,isentiments,ilinks=india.passon()
tsize,tsummary,ttitles,tsentiments,tlinks=tech.passon()
esize,esummary,etitles,esentiments,elinks=education.passon()
tnsize,tnsummary,tntitles,tnsentiments,tnlinks=topnews.passon()


p_size, n_size, neg_size = 0, 0 ,0
p_isize, n_isize, neg_isize = 0, 0 ,0
p_tsize, n_tsize, neg_tsize = 0, 0 ,0
p_esize, n_esize, neg_esize = 0, 0 ,0
p_tnsize, n_tnsize, neg_tnsize = 0, 0 ,0

for i in art_sentiments:
    if i == 'Positive' or i == 'positive':
        p_size += 1
    elif i == 'Neutral' or i =='neutral':
        n_size += 1
    else:
        neg_size += 1

for j in isentiments:
    if j == 'Positive' or j == 'positive':
        p_isize += 1
    elif j == 'Neutral' or j =='neutral':
        n_isize += 1
    else:
        neg_isize += 1

for k in tsentiments:
    if k == 'Positive' or k == 'positive':
        p_tsize += 1
    elif k == 'Neutral' or k =='neutral':
        n_tsize += 1
    else:
        neg_tsize += 1

for l in esentiments:
    if l == 'Positive' or l == 'positive':
        p_tsize += 1
    elif l == 'Neutral' or l =='neutral':
        n_esize += 1
    else:
        neg_esize += 1

for m in tnsentiments:
    if m == 'Positive' or i == 'positive':
        p_tnsize += 1
    elif m == 'Neutral' or i =='neutral':
        n_tnsize += 1
    else:
        neg_tnsize += 1

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/summary')
def summary():
    return render_template('summary.html', size = size, art_summary = art_summary, art_titles = art_titles, art_sentiments = art_sentiments, art_links = art_links,p_size = p_size, n_size = n_size, neg_size = neg_size)

@app.route('/indiasummary')
def indiasummary():
    return render_template('indiasummary.html', isize = isize, isummary = isummary, ititles = ititles, isentiments = isentiments, ilinks = ilinks,p_isize = p_isize, n_isize = n_isize, neg_isize = neg_isize)    

@app.route('/techsummary')
def techsummary():
    return render_template('techsummary.html', tsize = tsize, tsummary = tsummary, ttitles = ttitles, tsentiments = tsentiments, tlinks = tlinks,p_tsize = p_tsize, n_tsize = n_tsize, neg_tsize = neg_tsize)  

@app.route('/edusummary')
def edusummary():
    return render_template('edusummary.html', esize = esize, esummary = esummary, etitles = etitles, esentiments = esentiments, elinks = elinks,p_esize = p_esize, n_esize = n_esize, neg_esize = neg_esize)         
if __name__ == "__main__":
    app.run(debug=True)


@app.route('/topnewssummary')
def topnewssummary():
    return render_template('topnewssummary.html', tnsize = tnsize, tnsummary = tnsummary, tntitles = tntitles, tnsentiments = tnsentiments, tnlinks = tnlinks,p_tnsize = p_tnsize, n_tnsize = n_tnsize, neg_tnsize = neg_tnsize)         
if __name__ == "__main__":
    app.run(debug=True)
