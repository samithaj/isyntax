from dbcreator.models import *
from dbcreator.core import *


class PrimaryExtractor:
    def execute(self, tagged_sents, chunked_sents, target):
        pass


class SecondaryExtractor:
    def execute(self, entities):
        pass


class PossessionBasedExtractor(PrimaryExtractor):
    def execute(self, tagged_sents, chunked_sents, target):

        for sIndex, sent in enumerate(tagged_sents):
            # print(ne_chunked_sents)
            # ne_chunked_sent = ne_chunked_sents[sIndex]
            # print(ne_chunked_sent)
            # print(sent)
            for index, item in enumerate(sent):
                if ((item[0] == 'has' or item[0] == 'have')):
                    hIndex = item[2]
                    candidateEntityNames = [chunk for chunk in chunked_sents[sIndex] if chunk[0][2] < hIndex]

                    entityName = candidateEntityNames.pop()

                    candidateAttributeData = [chunk for chunk in chunked_sents[sIndex] if chunk[0][2] > hIndex]

                    attributes = []

                    for chunk in candidateAttributeData:
                        attr = Attribute(chunk)
                        attributes.append(attr)

                    entity = Entity(entityName)
                    entity.setAttributes(attributes)
                    target.append(entity)
                    break

                # if (item[1] == 'PRP'):
                #     pass


                elif item[1] == 'POS':
                    posIndex = sent[index-1][2]
                    candidateAttributeData = [chunk for chunk in chunked_sents[sIndex] if chunk[0][2] > posIndex]
                    attributes = []

                    for chunk in candidateAttributeData:
                        attr = Attribute(chunk)
                        attributes.append(attr)

                    entity = Entity([sent[index-1]])
                    entity.setAttributes(attributes)
                    target.append(entity)
                    break


class UniqueKeyExtractor(SecondaryExtractor):
    def execute(self, entities):
        for entity in entities:

            for attr in entity.getAttributes():
                isUnique = False
                isPrimaryKey = False
                isNotNull = False
                tempData = []
                for i, word in enumerate(attr.data):
                    if(word[0].lower() in ['unique','distinguishable','distinct']):
                        isUnique = True
                        isPrimaryKey = True
                        isNotNull = True
                    else:
                        tempData.append(word)
                attr.data = tempData
                attr.isUnique = isUnique
                attr.isPrimaryKey = isPrimaryKey
                attr.isNotNull = isNotNull


class IdentifyAttributeDataType(SecondaryExtractor):
    def execute(self, entities):

        intList = ['number', 'no', 'id', 'SSN']
        dateList = ['date', 'dob']
        doubleList = ['temperature', 'price', 'distance', 'weight', 'fee']

        for entity in entities:
            attrList = entity.getAttributes()
            for attr in attrList:
                for item in intList:
                    if item.lower() in attr.name().lower():
                        attr.dtype = DataType.INTEGER
                    if 'phone' in attr.name().lower():
                        attr.dtype = DataType.VARCHAR
                for item in dateList:
                    if item.lower() in attr.name().lower():
                        attr.dtype = DataType.DATETIME
                for item in doubleList:
                    if item.lower() in attr.name().lower():
                        attr.dtype = DataType.DOUBLE


class RemoveDuplicateEntities(SecondaryExtractor):
    def execute(self, entities):
        uniqueEntities = []

        for entity in entities:
            check = True
            for e in uniqueEntities:
                if e.name() == entity.name():
                    e.getAttributes().extend(entity.getAttributes())
                    check = False
                    break

            if check:
                uniqueEntities.append(entity)

        entities[:] = uniqueEntities[:]


class RemoveDuplicateAttributes(SecondaryExtractor):
    def execute(self, entities):

        for entity in entities:
            attrList = entity.getAttributes()
            compList = []
            for i, attr1 in enumerate(attrList):
                for j, attr2 in enumerate(attrList):
                    if(i!=j and set([i,j]) not in compList and attr1.name() == attr2.name()):
                        attrList.remove(attr2)

                    compList.append(set([i,j]))

            for attr in attrList:
                if attr.name() == '%':
                    attrList.remove(attr)

        # uniqueAttributes = []
        # for attr in attrList:
        #         check = True
        #         for a in uniqueAttributes:
        #             print(a.name())
        #             if a.name() == attr.name() or attr.name() == '%':
        #                 check = False
        #                 break
        #
        #     if check:
        #         uniqueAttributes.append(attr)
        #
        # attrList[:] = uniqueAttributes[:]


class RemoveNonPotentialEntities(SecondaryExtractor):
    def execute(self, entities):
        nonPotentialList = csv_reader('../knowledge_base/nonpotential_entities.csv')
        filteredList = []

        for entity in entities:
            check = True
            for item in nonPotentialList:
                if entity.name().lower() == item.lower():
                    check = False

            if check:
                filteredList.append(entity)

        entities[:] = filteredList[:]


# class SuggestRelationshipTypes(SecondaryExtractor):
#     def execute(self, entities):
#
#         removingList = []
#
#         for entity in entities:
#             check = True
#             attrList = entity.getAttributes()
#             for attr in attrList:
#                 if entity.name().lower() == attr.name().lower():
#                     check = False
#                     break
#
#             if check:
#                 removingList.append(attr)
#
#         attrList[:] = removingList[:]

# class RemoveAttributesFromEntityList(SecondaryExtractor):
#     def execute(self, entities):
#
#         removingIndex = []
#         for entity in entities:
#             attrList = entity.getAttributes()
#             for attr in attrList:
#                 for i, ent in enumerate(entities):
#                     if(attr.name() == ent.name()):
#                         removingIndex.append(i)
#
#         for i in set(removingIndex):
#             e = entities[i]
#             # print(e.name())
#             # entities.remove(e)


# class RemoveAttributesInEntityList(SecondaryExtractor):
#     def execute(self, entities):
#         for entity in entities:
#             for attr in entity.getAttributes():
#                 if attr in entities:
#                     entities.remove(attr)

















