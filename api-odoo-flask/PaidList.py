from Data import Data
import ssl
import json
import xmlrpc.client
from datetime import date
class PaidList:
    def __init__(self):
        self.username = 'admin' #the user
        self.pwd = 'Valerza2020' #the user
        self.dbname = 'valersa'    #the database
        self.uid = 0
        self.url = 'http://54.211.171.131:8069' #url
    def getConnection(self):
        gcontext = ssl._create_unverified_context()
        sock_common = xmlrpc.client.ServerProxy (self.url+'/xmlrpc/common',context=gcontext)
        self.uid = sock_common.login(self.dbname, self.username, self.pwd)
        return xmlrpc.client.ServerProxy(self.url+'/xmlrpc/object',context=gcontext)
    def getAmountsAvailabe(self):
        sock = self.getConnection()
        investment_ids = sock.execute(self.dbname,self.uid,self.pwd,'crm.investment','search',[('state','=','confirmed'), ('re_egreso', '>', 0)])
        dataList = []
        list = []
        count = 0
        print('cantidad de elementos '+ str(len(investment_ids)))
        for investment_id in investment_ids:
            investment_data = sock.execute(self.dbname,self.uid,self.pwd,'crm.investment','read',investment_id,['name','cuit','partner_id', 'currency_id', 'write_date', 're_egreso', 're_egreso_pago', 'cbu'])
            partner_data = sock.execute(self.dbname,self.uid,self.pwd,'res.partner','read',investment_data[0]['partner_id'][0],['name', 'cuit']) 
            index = [i for i in range(len(dataList)) if dataList[i].partnerId == investment_data[0]['partner_id'][0]] 
            if len(index) > 0:
                if investment_data[0]['re_egreso_pago'] == 'Transferencia':
                    if investment_data[0]['currency_id'][0] == 3: #USD
                        dataList[index[0]].availableUSDTransfer = dataList[index[0]].availableUSDTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            dataList[index[0]].cbuUSD = str(investment_data[0]['cbu'])
                    else:
                        dataList[index[0]].availableARSTransfer = dataList[index[0]].availableARSTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            dataList[index[0]].cbuARS = str(investment_data[0]['cbu'])
                else:
                    if investment_data[0]['re_egreso_pago'] == 'Ventanilla':
                        if investment_data[0]['currency_id'][1] == 'USD':
                            dataList[index[0]].availableUSDATM = dataList[index[0]].availableUSDATM + investment_data[0]['re_egreso']
                        else:
                            dataList[index[0]].availableARSATM = dataList[index[0]].availableARSATM + investment_data[0]['re_egreso']
            else:
                data = Data()
                data.cbuARS = '-'
                data.cbuUSD = '-'
                data.cuit = partner_data[0]['cuit']
                data.nombre = partner_data[0]['name']
                data.partnerId = investment_data[0]['partner_id'][0]
                data.availableUSDTransfer = 0
                data.availableARSTransfer = 0
                data.availableUSDATM = 0
                data.availableARSATM = 0
                if investment_data[0]['re_egreso_pago'] == 'Transferencia':
                    if investment_data[0]['currency_id'][0] == 3: #USD
                        data.availableUSDTransfer = data.availableUSDTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            data.cbuUSD = str(investment_data[0]['cbu'])
                    else:
                        data.availableARSTransfer = data.availableARSTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            data.cbuARS = str(investment_data[0]['cbu'])
                else:
                    if investment_data[0]['re_egreso_pago'] == 'Ventanilla':
                        if investment_data[0]['currency_id'][0] == 3:
                            data.availableUSDATM = data.availableUSDATM + investment_data[0]['re_egreso']
                        else:
                            data.availableARSATM = data.availableARSATM + investment_data[0]['re_egreso']
                dataList.append(data)
        for element in dataList:
            row = {
                'CUIT': str(element.cuit),
                'CLIENTE': element.nombre,
                'MONTO_ARS_TRANSFER': str(element.availableARSTransfer),
                'MONTO_USD_TRANSFER': str(element.availableUSDTransfer),
                'MONTO_ARS_ATM': str(element.availableARSATM),
                'MONTO_USD_ATM': str(element.availableUSDATM),
                'CBU_ARS': element.cbuARS,
                'CBU_USD': element.cbuUSD,
                'PARTNER_ID': element.partnerId
            }
            list.append(row)
        return json.dumps(list)
    def exportARS(self, list):
        exportFile = []
        dataList = json.loads(list)
        counter = 0
        totalAmount = 0
        header = 'RC,PAGO,30714470775,,,,,,,,'
        row = {
            'header': header
        }
        body = ''
        exportFile.append(row)
        for element in dataList:
            if float(element['MONTO_ARS_TRANSFER']) > 0:
                counter += 1
                totalAmount += float(element['MONTO_ARS_TRANSFER'])
                body = 'RT,' + str(counter)
                body += ','+ str(element['PARTNER_ID'])
                body += ',' + element['CUIT']
                body += ',' + element['CLIENTE']
                body += ',' + element['CBU_ARS']
                body += ',' + date.today().strftime('%d/%m/%Y')
                body += ',$'
                body += ',' + str(float(element['MONTO_ARS_TRANSFER']))
                body += ',,'
                row = {
                    'body': body
                }
                exportFile.append(row)
                
        footer = 'RF, '+ str(counter)+', '+ str(totalAmount)+ ',,,,,,,,'
        row = {
            'footer': footer
        }
        exportFile.append(row)
        return json.dumps(exportFile)
    def exportUSD(self, list):
        exportFile = []
        dataList = json.loads(list)
        counter = 0
        totalAmount = 0
        header = 'RC,PAGO,30714470775,,,,,,,,'
        row = {
            'header': header
        }
        body = ''
        dateNow = date.today()
        exportFile.append(row)
        for element in dataList:
            if float(element['MONTO_USD_TRANSFER']) > 0:
                counter += 1
                totalAmount += float(element['MONTO_ARS_TRANSFER'])
                body = 'RT,' + str(counter)
                body += ','+ str(element['PARTNER_ID'])
                body += ',' + element['CUIT']
                body += ',' + element['CLIENTE']
                body += ',' + element['CBU_USD']
                body += ',' + date.today().strftime('%d/%m/%Y')
                body += ',$'
                body += ',' + str(float(element['MONTO_USD_TRANSFER']))
                body += ',,'
                row = {
                    'body': body
                }
                exportFile.append(row)
                
        footer = 'RF, '+ str(counter)+', '+ str(totalAmount)+ ',,,,,,,,'
        row = {
            'footer': footer
        }
        exportFile.append(row)
        return json.dumps(exportFile)