from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect,HttpResponse
from django.core.files.storage import FileSystemStorage
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



import os
import sys
def index(request):
    return render(request,"index.html")




def clean(words):
    return dict([(word, True) for word in words])




def process(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['data']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
      
        f = open('model', 'rb')
        classifier = pickle.load(f)
        f.close()
        opinion = {}

        f = open('user_data/'+uploaded_file.name, 'r')
        pos, neg = 0, 0
        for line in f:
            print(line)
            try:
                chat = line.split('-')[1].split(':')[1]
                name = line.split('-')[1].split(':')[0]
                if opinion.get(name, None) is None:
                    opinion[name] = [0, 0]
                res = classifier.classify(clean(chat))
                print(name, res, chat)
                if res == 'positive':
                    pos += 1
                    opinion[name][0] += 1
                else:
                    neg += 1
                    opinion[name][1] += 1
            except:
                pass

        neg = abs(neg)
        labels = ['positive', 'negative']
        sizes = [pos, neg]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Whatsapp Sentiment Analysis Overall')







        print(pos,neg)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

       # return render(request, 'graphic.html', {'graphic': graphic})





        names, positive, negative = [], [], []
        for name in opinion:
            names.append(name)
            positive.append(opinion[name][0])
            negative.append(opinion[name][1])
        ind = np.arange(len(names))
        width = 0.3
        max_x = max(max(positive), max(negative)) + 2

        fig = plt.figure()
        ax = fig.add_subplot()

        yvals = positive
        rects1 = ax.bar(ind, yvals, width, color='g')
        zvals = negative
        rects2 = ax.bar(ind + width, zvals, width, color='r')

        ax.set_xlabel('Names')
        ax.set_ylabel('Sentiment')

        ax.set_xticks(ind + width)
        ax.set_yticks(np.arange(0, max_x, 1))
        ax.set_xticklabels(names,rotation=90)
        ax.legend((rects1[0], rects2[0]), ('positive', 'negative'))
        ax.set_title('Whatsapp Chat Sentiment Analysis Individual')
        fig.set_size_inches(35, 15, forward=True)


        for rect in rects1:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                    ha='center', va='bottom')

        for rect in rects2:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                    ha='center', va='bottom')

        buffer2 = BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        image_png2 = buffer2.getvalue()
        buffer2.close()

        graphic2 = base64.b64encode(image_png2)
        graphic2 = graphic2.decode('utf-8')

        return render(request, 'graphic.html', {'full': graphic,'indi':graphic2})

    return render(request, "index.html")





def youtube(request):
    if request.method == 'POST':
        link = request.POST.get('link',None)
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(link)
        wait = WebDriverWait(driver, 10)
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
        i = 5
        while i:
            driver.execute_script('window.scrollTo(1, 5000);')
            time.sleep(3)
            driver.execute_script('window.scrollTo(1, 30000);')
            i -= 1
            print(i)

        comment_div = driver.find_element_by_xpath('//*[@id="contents"]')
        comments = comment_div.find_elements_by_xpath('//*[@id="content-text"]')
        print(len(comments))
        pos, neg = 0, 0
        f = open('model', 'rb')
        classifier = pickle.load(f)
        f.close()
        for comment in comments:
            sentence = comment.text
            features = clean(sentence)
            res = classifier.classify(features)
            if res == 'positive':
                pos += 1
            else:
                neg += 1

        print(pos, neg)
        neg = abs(neg)
        labels = ['positive', 'negative']
        sizes = [pos, neg]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Youtube Comment Sentiment Analysis')
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        return render(request, 'yto.html', {'graphic': graphic,'title':title})
    return render(request, "ytin.html")


