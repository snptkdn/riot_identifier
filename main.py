import discord
from discord import app_commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('cred.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

TOKEN = "MTE5NzUwNjQzNjE3MTgzNzUxMQ.G994qr.eSWuNq7CnOosaIyEG9BQpDoRlhI4PCRDBpleJo"

intents = discord.Intents.default()#適当に。
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期
    
@tree.command(name="add_user",description="Riotのユーザーを追加します。ex)name:t3RR4p1N tag:1234")
async def add_command(interaction: discord.Interaction, name: str, tag: int):
    data = {"discord_id": interaction.user.id, "riot_id": name + "#" + str(tag)}

    db.collection("riot_user").document(str(interaction.user.id)).set(data)
    await interaction.response.send_message(name + "#" + str(tag) + "を登録しました〜きゅんっ",ephemeral=True)
    
@tree.command(name="delete_user",description="自分に紐づいているRiotのユーザーを削除します。")
async def delete_command(interaction: discord.Interaction):
    # ユーザーIDに紐づいているデータを取得
    doc_ref = db.collection("riot_user").document(str(interaction.user.id))
    doc = doc_ref.get()
    
    db.collection("riot_user").document(str(interaction.user.id)).delete()
    
    # 消したデータを返す
    await interaction.response.send_message(doc.to_dict()["riot_id"] + "を削除しました〜きゅんっ",ephemeral=True)

@tree.command(name="get_user",description="自分に紐づいているRiotのユーザーを取得します。")
async def get_command(interaction: discord.Interaction):
    # ユーザーIDに紐づいているデータを取得
    doc_ref = db.collection("riot_user").document(str(interaction.user.id))
    doc = doc_ref.get()
    
    # データを返す
    await interaction.response.send_message(doc.to_dict()["riot_id"] + "が紐づいてるユーザーだよ〜きゅんっ",ephemeral=True)

client.run(TOKEN)
