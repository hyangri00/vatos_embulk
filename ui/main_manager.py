# https://doc.qt.io/qtforpython-5/tutorials/basictutorial/uifiles.html
# https://hello-bryan.tistory.com/407
# https://onlytojay.medium.com/pyside2로-간단한-calcultor-exe-만들기-3cf247b21f6e

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import module.common as cm
import cx_Oracle

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' # 디스플레이 설정에 따라 변하게
UI_FILE_PATH = fr"{cm.ROOT_PATH}\ui\main.ui"

class MainWindow(QObject):
    def __init__(self, uiFileName, parent=None):
        super(MainWindow, self).__init__(parent)
        uiFile = QFile(uiFileName)
        uiFile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()

        # ================= 접속 정보 입력 및 접속 버튼 [START] ==================================

        # UI에 연결할 변수를 선언
        self.le_ip = self.__bindQLineEdit('lineEditSrcHost')
        self.le_port = self.__bindQLineEdit('lineEditSrcPort')
        self.le_sid = self.__bindQLineEdit('lineEditSrcDB')
        self.le_id = self.__bindQLineEdit('lineEditSrcUser')
        self.le_pw = self.__bindQLineEdit('lineEditSrcPasswd')
        self.le_pw.setEchoMode(QLineEdit.Password)                          # 패스워드 마스킹
        self.btn_connect = self.__bindQPushButton('pushButtonSrcTestConn')
        self.btn_connect = self.__bindQPushButton('pushButtonSrcConn')

        # 버튼 클릭 시 실행될 함수를 연결
        self.btn_test_conn = self.__bindQPushButton('pushButtonSrcTestConn')
        self.btn_test_conn.clicked.connect(self.__testConnDb)

        self.btn_connect = self.__bindQPushButton('pushButtonSrcConn')
        self.btn_connect.clicked.connect(self.__ConnDb)

        # ================= 접속 정보 입력 및 접속 버튼 [END] ==================================

        # 윈도우를 화면에 표시
        self.setup_ui()
        self.window.show()
    
<<<<<<< HEAD
    # ================= 접속 및 테이블리스트 추가 [START] ==================================
=======
    # ================= 테스트 접속 [START] ==================================
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
    def __testConnDb(self):
        # 입력된 오라클 정보를 매핑
        user_id = self.le_id.text()
        user_pw = self.le_pw.text()
        ip = self.le_ip.text()
        port = self.le_port.text()
        sid = self.le_sid.text()

        try:
            # 데이터베이스 연결 정보를 설정
            dsn = cx_Oracle.makedsn(ip, port, sid)
            conn = cx_Oracle.connect(user_id, user_pw, dsn)

            # 성공 텍스트 팝업
            QMessageBox.information(
                self.window, 'Message',
                '성공적으로 연결되었습니다.',
                QMessageBox.Ok
            )

            # 연결을 종료
            conn.close()

        except cx_Oracle.DatabaseError as e:
            # 실패 텍스트 팝업
            QMessageBox.warning(
                self.window, 'Message',
                f'연결 실패: {e}',
                QMessageBox.Ok
            )
<<<<<<< HEAD

=======
    # ================= 테스트 접속 [END] ==================================

    # ================= 접속 및 테이블리스트 추가 [START] ==================================
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
    def __ConnDb(self):
        # pushButtonSrcTestConn 와 동일한 함수 구현
        user_id = self.le_id.text()
        user_pw = self.le_pw.text()
        ip = self.le_ip.text()
        port = self.le_port.text()
        sid = self.le_sid.text()

        try:
            dsn = cx_Oracle.makedsn(ip, port, sid)
            conn = cx_Oracle.connect(user_id, user_pw, dsn)

            # 성공 텍스트 팝업
            QMessageBox.information(
                self.window, 'Message',
                '성공적으로 연결되었습니다.',
                QMessageBox.Ok
            )
            
            # 커서 생성 및 쿼리를 실행
            cursor = conn.cursor()
            rows = cursor.execute(cm.getTblList()).fetchall()

            # 반환할 QTreeWidget 생성
            table_tree = self.__bindQTreeWidget("treeViewMigTables")
            table_tree.clear()
            table_tree = self.__bindQTreeWidget("treeViewSrcTables")
            table_tree.clear()
            table_tree.setColumnCount(3)
            table_tree.setHeaderLabels(["Owner", "Table Name", "Partition Name"])
        
            # 트리 아이템 추가
            for row in rows:
                owner = row[0]
                table_name = row[1]
                partition = row[2] # or "N/A"
        
                owner_item = table_tree.findItems(owner, Qt.MatchExactly | Qt.MatchRecursive, 0)[0] if table_tree.findItems(owner, Qt.MatchExactly | Qt.MatchRecursive, 0) else QTreeWidgetItem(table_tree, [owner])
                table_item = table_tree.findItems(table_name, Qt.MatchExactly | Qt.MatchRecursive, 0)[0] if table_tree.findItems(table_name, Qt.MatchExactly | Qt.MatchRecursive, 0) else QTreeWidgetItem(owner_item, [table_name])
                if partition:
                    partition_item = QTreeWidgetItem(table_item, [partition])
        
            # 연결을 종료
            conn.close()
        except cx_Oracle.DatabaseError as e:
            # 실패 텍스트 팝업
            QMessageBox.warning(
                self.window, 'Message',
                f'연결 실패: {e}',
                QMessageBox.Ok
            )

    # ================= 접속 및 테이블리스트 추가 [END] ==================================

    def setup_ui(self):
        self.treeSrcTab = self.__bindQTreeWidget('treeViewSrcTables')
        self.treeMigTab = self.__bindQTreeWidget('treeViewMigTables')
        self.pbPlus = self.__bindQPushButton('pushButtonPlus')
        self.pbMinus = self.__bindQPushButton('pushButtonMinus')
        self.pbPlus.clicked.connect(self.copy_item)
        self.pbMinus.clicked.connect(self.remove_item)

    def __bindQLineEdit(self, objectName):
        return self.window.findChild(QLineEdit, objectName)
    
    def __bindQLabel(self, objectName):
        return self.window.findChild(QLabel, objectName)
    
    def __bindQPlainTextEdit(self, objectName):
        return self.window.findChild(QPlainTextEdit, objectName)
    
    def __bindQComboBox(self, objectName):
        return self.window.findChild(QComboBox, objectName)
    
    def __bindQTreeWidget(self, objectName):
        return self.window.findChild(QTreeWidget, objectName)
    
    def __bindObject(self, qType, objectName):
        return self.window.findChild(qType, objectName)

    def __bindQPushButton(self, objectName):
        btn = self.window.findChild(QPushButton, objectName)
        # 버튼 클릭했을 때 click_objectName 함수 호출
        #eval(f'btn.clicked.connect(self.click_{objectName})')
        return btn
    
    def find_item(self, treeList, item):
        count = treeList.topLevelItemCount()
        for i in range(count):
            if item.text(0) == treeList.topLevelItem(i).text(0):
                return i
            
        return -1
    
    def find_child_items(self, parent_item, selected_item):
        count = parent_item.childCount()
        for i in range(count):
            child_item = parent_item.child(i)
            if selected_item.text(0) == child_item.text(0):
                return i
        return -1
<<<<<<< HEAD

=======
    
    # ================= 트리 추가 제거 [START] ==================================
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
    def copy_item(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab

        selected_items = srcTreeList.selectedItems()

        # 선택했음
        for item in selected_items:
            parent_item = item.parent()
            grandparent_item = parent_item.parent() if parent_item is not None else None
            child_count = item.childCount()
            copied_item = item.clone()

<<<<<<< HEAD
            # 최상단(Schema) 항목일 때
=======
            # 최상단 항목일 때
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
            if parent_item is None:
                if self.find_item(tgtTreeList, copied_item) < 0:
                    tgtTreeList.addTopLevelItem(copied_item)

<<<<<<< HEAD
            # 중간(Table) 항목일 때
            elif child_count > 0:
                copied_parent_item = parent_item.clone()
                copied_parent_item.takeChildren()
                
                # 트리뷰를 탐색해서 같은 스키마가 있는지 탐색
                retrunIdx = self.find_item(tgtTreeList, copied_parent_item)
        
                # 새로운 스키마인 경우
                if retrunIdx < 0:
                    tgtTreeList.addTopLevelItem(copied_parent_item)
                    tgtTreeList.topLevelItem(tgtTreeList.indexOfTopLevelItem(copied_parent_item)).addChild(copied_item)
                
                # 이미 추가된 스키마인 경우
=======
            # 2) 중간 항목일 때
            elif child_count > 0:
                copied_parent_item = parent_item.clone()
                copied_parent_item.takeChildren()
        
                retrunIdx = self.find_item(tgtTreeList, copied_parent_item)
        
                if retrunIdx < 0:
                    tgtTreeList.addTopLevelItem(copied_parent_item)
                    tgtTreeList.topLevelItem(tgtTreeList.indexOfTopLevelItem(copied_parent_item)).addChild(copied_item)
        
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
                else:
                    target_parent_item = tgtTreeList.topLevelItem(retrunIdx)
                    if self.find_child_items(target_parent_item, copied_item) < 0:
                        target_parent_item.addChild(copied_item)

<<<<<<< HEAD
            # 최하위(Partition) 항목일 때
            else:
                if child_count == 0:  # 하위 항목이 없는 경우
                    copied_parent_item = parent_item.clone()  # 복사할 부모 항목
                    copied_parent_item.takeChildren()  # 복사된 부모 항목의 하위 항목 제거
                    return_idx = self.find_item(tgtTreeList, copied_parent_item)  # 복사된 부모 항목 중에서 같은 스키마가 있는 항목 탐색
            
=======
            # 하위 항목일 때
            else:
                if child_count == 0:
                    copied_parent_item = parent_item.clone()
                    copied_parent_item.takeChildren()
                    return_idx = self.find_item(tgtTreeList, copied_parent_item)

>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
                    # 같은 스키마가 없을 때
                    if return_idx < 0:
                        if grandparent_item is not None:  # 부모와 조부모 항목이 모두 있는 경우
                            copied_grandparent_item = grandparent_item.clone()
                            copied_grandparent_item.takeChildren()
                            grandparent_return_idx = self.find_item(tgtTreeList, copied_grandparent_item)
<<<<<<< HEAD
            
                            # 조부모 항목도 새로운 스키마인 경우
                            if grandparent_return_idx < 0:
                                # 조부모 항목을 추가하고, 부모 항목을 조부모 항목 밑으로 추가
                                tgtTreeList.addTopLevelItem(copied_grandparent_item)
                                tgtTreeList.topLevelItem(tgtTreeList.indexOfTopLevelItem(copied_grandparent_item)).addChild(copied_parent_item)

                                # 부모 항목 아래에 하위 항목을 추가
                                copied_parent_item.addChild(copied_item)

                            else:
                                # 조부모 항목 아래에 부모 항목을 추가
                                tgtTreeList.topLevelItem(grandparent_return_idx).addChild(copied_parent_item)
            
                            # 부모 항목 아래에 하위 항목을 추가
                            if self.find_child_items(copied_parent_item, copied_item) < 0:
                                copied_parent_item.addChild(copied_item)
                        else:
                            # 부모 항목을 새로운 스키마로 추가하고, 그 아래에 하위 항목을 추가
                            tgtTreeList.addTopLevelItem(copied_parent_item)
                            if self.find_child_items(copied_parent_item, copied_item) < 0:
                                copied_parent_item.addChild(copied_item)
            
                    # 같은 스키마가 있을 때
                    else:
                        target_parent_item = tgtTreeList.topLevelItem(return_idx)
                        # 부모 항목 아래에 하위 항목이 존재하지 않으면 추가
=======

                            if grandparent_return_idx < 0:
                                tgtTreeList.addTopLevelItem(copied_grandparent_item)
                                tgtTreeList.topLevelItem(tgtTreeList.indexOfTopLevelItem(copied_grandparent_item)).addChild(copied_parent_item)
                            else:
                                tgtTreeList.topLevelItem(grandparent_return_idx).addChild(copied_parent_item)

                            # 그 아래에 하위 항목 추가
                            if self.find_child_items(copied_parent_item, copied_item) < 0:
                                copied_parent_item.addChild(copied_item)
                        else:
                            tgtTreeList.addTopLevelItem(copied_parent_item)
                            if self.find_child_items(copied_parent_item, copied_item) < 0:
                                copied_parent_item.addChild(copied_item)

                    # 있으면 그 아래에 하위 항목만 추가
                    else:
                        target_parent_item = tgtTreeList.topLevelItem(return_idx)
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a
                        if self.find_child_items(target_parent_item, copied_item) < 0:
                            target_parent_item.addChild(copied_item)

    def remove_item(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab

        selected_items = srcTreeList.selectedItems()

        for item in selected_items:
            parent_item = item.parent()
            if parent_item is not None:
                if parent_item.childCount() == 1:
                    index = srcTreeList.indexOfTopLevelItem(parent_item)
                    srcTreeList.takeTopLevelItem(index)
                parent_item.removeChild(item)
            else:
                index = srcTreeList.indexOfTopLevelItem(item)
                srcTreeList.takeTopLevelItem(index)
<<<<<<< HEAD
=======
    # ================= 트리 추가 제거 [END] ==================================
>>>>>>> e569e29f670742ef5213cf78b3d3f5831348f85a

    # 지워진 이력 확인. 용도 확인 필요.
    def clickMoveItem(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab
        item = srcTreeList.takeTopLevelItem(srcTreeList.currentColumn())
        root = QTreeWidget.invisibleRootItem(tgtTreeList)
        root.addChild(item)

def exec():
    app = QApplication(sys.argv)
    form = MainWindow(UI_FILE_PATH)

    sys.exit(app.exec_())