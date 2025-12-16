import requests
from bs4 import BeautifulSoup
import csv

# 请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 存储所有高校信息的列表
universities = []

def crawl_page(page_num):
    """爬取指定页码的大学排名数据"""
    # 软科中国大学排名的列表页URL（支持翻页）
    url = f"https://www.shanghairanking.cn/rankings/best-chinese-universities/{page_num}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 抛出HTTP错误
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 定位排名表格的行（排除表头）
        rows = soup.select("table tr")[1:]
        if not rows:
            return False  # 没有数据则停止翻页
        
        for row in rows:
            # 提取排名、学校名称、总分等信息
            cols = row.select("td")
            rank = cols[0].text.strip()  # 排名
            name = cols[1].text.strip()  # 学校名称
            score = cols[2].text.strip()  # 总分
            province = cols[3].text.strip()  # 省份
            type_ = cols[4].text.strip()  # 学校类型
            category = cols[5].text.strip()  # 办学层次
            
            # 将信息存入列表
            universities.append({
                "排名": rank,
                "学校名称": name,
                "总分": score,
                "省份": province,
                "学校类型": type_,
                "办学层次": category
            })
        print(f"第{page_num}页爬取完成，共{len(rows)}条数据")
        return True
    except Exception as e:
        print(f"爬取第{page_num}页失败：{e}")
        return False

def main():
    """主函数：翻页爬取所有数据并保存为CSV"""
    page = 1
    # 循环翻页，直到没有数据为止
    while crawl_page(page):
        page += 1
    
    # 将数据保存为CSV文件
    if universities:
        with open("中国大学排名.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=universities[0].keys())
            writer.writeheader()
            writer.writerows(universities)
        print(f"\n爬取完成！共获取{len(universities)}所高校信息，已保存至「中国大学排名.csv」")
    else:
        print("未爬取到任何高校数据")

if __name__ == "__main__":
    main()

