from flask import Flask, jsonify, request
from sklearn.externals import joblib
import cv2
import os
import pytesseract
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import requests
from flask_cors import CORS, cross_origin
import pycurl
from io import BytesIO
from aylienapiclient import textapi

client = textapi.Client("ec8bc26c", "924edfc4ca5194b66477ca27257ab13e")

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.0.0/bin/tesseract'

app = Flask(__name__)
CORS(app)

textsum="""Grimm's Fairy Tale version - translated by Margaret Hunt - language modernized a bit by Leanne Guenther

snow white
Once upon a time, long, long ago a king and queen ruled over a distant land.  The queen was kind and lovely and all the people of the realm adored her.  The only sadness in the queen's life was that she wished for a child but did not have one. 

One winter day, the queen was doing needle work while gazing out her ebony window at the new fallen snow.  A bird flew by the window startling the queen and she pricked her finger.  A single drop of blood fell on the snow outside her window.  As she looked at the blood on the snow she said to herself, "Oh, how I wish that I had a daughter that had skin as white as snow, lips as red as blood, and hair as black as ebony."  

Soon after that, the kind queen got her wish when she gave birth to a baby girl who had skin white as snow, lips red as blood, and hair black as ebony.  They named the baby princess Snow White, but sadly, the queen died after giving birth to Snow White.

Soon after, the king married a new woman who was beautiful, but as well proud and cruel.  She had studied dark magic and owned a magic mirror, of which she would daily ask, 

Mirror, mirror on the wall, who's the fairest of them all?

Each time this question was asked, the mirror would give the same answer, "Thou, O Queen, art the fairest of all."  This pleased the queen greatly as she knew that her magical mirror could speak nothing but the truth.

One morning when the queen asked, "Mirror, mirror on the wall, who's the fairest of them all?" she was shocked when it answered:

You, my queen, are fair; it is true.
But Snow White is even fairer than you.
The Queen flew into a jealous rage and ordered her huntsman to take Snow White into the woods to be killed.  She demanded that the huntsman return with Snow White's heart as proof. 

The poor huntsman took Snow White into the forest, but found himself unable to kill the girl.  Instead, he let her go, and brought the queen the heart of a wild boar.

Snow White was now all alone in the great forest, and she did not know what to do.  The trees seemed to whisper to each other, scaring Snow White who began to run.  She ran over sharp stones and through thorns.  She ran as far as her feet could carry her, and just as evening was about to fall she saw a little house and went inside in order to rest.

Inside the house everything was small but tidy.  There was a little table with a tidy, white tablecloth and seven little plates.  Against the wall there were seven little beds, all in a row and covered with quilts.

Because she was so hungry Snow White ate a few vegetables and a little bread from each little plate and from each cup she drank a bit of milk. Afterward, because she was so tired, she lay down on one of the little beds and fell fast asleep.

After dark, the owners of the house returned home.  They were the seven dwarves who mined for gold in the mountains.  As soon as they arrived home, they saw that someone had been there -- for not everything was in the same order as they had left it.

The first one said, "Who has been sitting in my chair?"

The second one, "Who has been eating from my plate?"

The third one, "Who has been eating my bread?"

The fourth one, "Who has been eating my vegetables?"

The fifth one, "Who has been eating with my fork?"

The sixth one, "Who has been drinking from my cup?"

But the seventh one, looking at his bed, found Snow White lying there asleep.  The seven dwarves all came running up, and they cried out with amazement.  They fetched their seven candles and shone the light on Snow White. 

"Oh good heaven! " they cried. "This child is beautiful!"

They were so happy that they did not wake her up, but let her continue to sleep in the bed.  The next morning Snow White woke up, and when she saw the seven dwarves she was frightened.  But they were friendly and asked, "What is your name?"

"My name is Snow White," she answered.

"How did you find your way to our house?" the dwarves asked further.

Then she told them that her stepmother had tried to kill her, that the huntsman had spared her life, and that she had run the entire day through the forest, finally stumbling upon their house.

The dwarves spoke with each other for awhile and then said, "If you will keep house for us, and cook, make beds, wash, sew, and knit, and keep everything clean and orderly, then you can stay with us, and you shall have everything that you want."

"Yes," said Snow White, "with all my heart."  For Snow White greatly enjoyed keeping a tidy home.

So Snow White lived happily with the dwarves.  Every morning they went into the mountains looking for gold, and in the evening when they came back home Snow White had their meal ready and their house tidy.  During the day the girl was alone, except for the small animals of the forest that she often played with.

Now the queen, believing that she had eaten Snow White's heart, could only think that she was again the first and the most beautiful woman of all.  She stepped before her mirror and said:

Mirror, mirror, on the wall,
Who in this land is fairest of all?

It answered:

You, my queen, are fair; it is true.
But Snow White, beyond the mountains
With the seven dwarves,
Is still a thousand times fairer than you.

This startled the queen, for she knew that the mirror did not lie, and she realized that the huntsman had deceived her and that Snow White was still alive.  Then she thought, and thought again, how she could rid herself of Snow White -- for as long as she was not the most beautiful woman in the entire land her jealousy would give her no rest.

At last she thought of something.  She went into her most secret room -- no one else was allowed inside -- and she made a poisoned apple.  From the outside it was beautiful, and anyone who saw it would want it.  But anyone who might eat a little piece of it would die.  Coloring her face, she disguised herself as an old peddler woman, so that no one would recognize her, traveled to the dwarves house and knocked on the door.

Snow White put her head out of the window, and said, "I must not let anyone in; the seven dwarves have forbidden me to do so."

"That is all right with me," answered the peddler woman. "I'll easily get rid of my apples.  Here, I'll give you one of them."

"No," said Snow White, "I cannot accept anything from strangers."

"Are you afraid of poison?" asked the old woman. "Look, I'll cut the apple in two.  You eat half and I shall eat half."

Now the apple had been so artfully made that only the one half was poisoned.  Snow White longed for the beautiful apple, and when she saw that the peddler woman was eating part of it she could no longer resist, and she stuck her hand out and took the poisoned half.  She barely had a bite in her mouth when she fell to the ground dead.

The queen looked at her with an evil stare, laughed loudly, and said, "White as snow, red as blood, black as ebony wood!  The dwarves shall never awaken you."

Back at home she asked her mirror:

Mirror, mirror, on the wall,
Who in this land is fairest of all?

It finally answered:

You, my queen, are fairest of all.

Then her cruel and jealous heart was at rest, as well as a cruel and jealous heart can be at rest.

When the dwarves came home that evening they found Snow White lying on the ground.  She was not breathing at all.  She was dead.  They lifted her up and looked at her longingly.  They talked to her, shook her and wept over her.  But nothing helped.  The dear child was dead, and she remained dead.  They laid her on a bed of straw, and all seven sat next to her and mourned for her and cried for three days.  They were going to bury her, but she still looked as fresh as a living person, and still had her beautiful red cheeks.

They said, "We cannot bury her in the black earth," and they had a transparent glass coffin made, so she could be seen from all sides.  They laid her inside, and with golden letters wrote on it her name, and that she was a princess.  Then they put the coffin outside on a mountain, and one of them always stayed with it and watched over her.  The animals too came and mourned for Snow White, first an owl, then a raven, and finally a dove.

Now it came to pass that a prince entered these woods and happened onto the dwarves' house, where he sought shelter for the night .  He saw the coffin on the mountain with beautiful Snow White in it, and he read what was written on it with golden letters.

Then he said to the dwarves, "Let me have the coffin.  I will give you anything you want for it."

But the dwarves answered, "We will not sell it for all the gold in the world."

Then he said, "Then give it to me, for I cannot live without being able to see Snow White.  I will honor her and respect her as my most cherished one."

As he thus spoke, the good dwarves felt pity for him and gave him the coffin.  The prince had his servants carry it away on their shoulders.  But then it happened that one of them stumbled on some brush, and this dislodged from Snow White's throat the piece of poisoned apple that she had bitten off.  Not long afterward she opened her eyes, lifted the lid from her coffin, sat up, and was alive again.

"Good heavens, where am I?" she cried out.

The prince said joyfully, "You are with me."  He told her what had happened, and then said, "I love you more than anything else in the world.  Come with me to my father's castle.  You shall become my wife."  Snow White loved him, and she went with him.  Their wedding was planned with great splendor and majesty.

Snow White's wicked step-mother was invited to the feast, and when she had arrayed herself in her most beautiful garments, she stood before her mirror, and said:

Mirror, mirror, on the wall,
Who in this land is fairest of all?

The mirror answered:
You, my queen, are fair; it is true.
But the young queen is a thousand times fairer than you.

Not knowing that this new queen was indeed her stepdaughter, she arrived at the wedding, and her heart filled with the deepest of dread when she realized the truth - the evil queen was banished from the land forever and the prince and Snow White lived happily ever after.

"""

@app.route('/deepai/djdjdjd')
def DeepAI():
# Example directly sending a text string:
    r = requests.post(
        "https://api.deepai.org/api/summarization",
        data={
            'text': textsum,
        },
        headers={'api-key': '42c8dc64-72f1-4343-8d89-4c437f054be9'}
    )
    a=r.json()
    return jsonify({'emp':a})


@app.route('/resoomer/djdjdjd')
def DeeAI():
    datasPost='API_KEY='+'7ECF774EC2A65DD4E90A6FD4F3F8D245'+'&text='+textsum
    response= BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'https://resoomer.pro/summarizer/')
    c.setopt(pycurl.POST, 2)
    c.setopt(pycurl.POSTFIELDS, datasPost)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.perform()
    content = response.getvalue().decode('UTF-8')
    return content

@app.route('/aylien/djdjdjd')
def mashable():   
    summary = client.Summarize({'title':'Title','text': textsum, 'sentences_percentage': 50})
    #for sentence in summary['sentences']:
     #   print(sentence)
    return jsonify({'emp':summary})

@app.route('/image/<img_path>')
def summariseimage(img_path):
    # Read image using opencv
   
    img = cv2.imread(img_path)
    

    # Extract the file name without the file extension
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]

    # Create a directory for outputs
    output_path = os.path.join('Save1', file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
      # Save the filtered image in the output directory
   # save_path = os.path.join(output_path, file_name + "_filter_" + str(method) + ".jpg")
   # cv2.imwrite(save_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img, lang="eng")
    r=[
        {
            'text':result
        }]
    return  jsonify({'emp':r})

@app.route('/pdf/<path>')
def summarisepdf(path):
    # Read image using opencv
   
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    r=[
        {
            'text':text
        }]
    return  jsonify({'emp':r})

if __name__ == '__main__':
   app.run(debug = True)